from math import asin, cos, radians, sin, sqrt
import re

from flask import Blueprint, jsonify, request
import requests

routes_bp = Blueprint('routes', __name__)
_geocode_cache = {}

LOCATIONS = {
    'port of rotterdam': {'name': 'Port of Rotterdam', 'lat': 51.9225, 'lng': 4.4792},
    'rotterdam': {'name': 'Port of Rotterdam', 'lat': 51.9225, 'lng': 4.4792},
    'munich hub': {'name': 'Munich Hub', 'lat': 48.1351, 'lng': 11.5820},
    'munich': {'name': 'Munich Hub', 'lat': 48.1351, 'lng': 11.5820},
    'shanghai port': {'name': 'Shanghai Port', 'lat': 31.2304, 'lng': 121.4737},
    'shanghai': {'name': 'Shanghai Port', 'lat': 31.2304, 'lng': 121.4737},
    'los angeles': {'name': 'Los Angeles', 'lat': 34.0522, 'lng': -118.2437},
    'la': {'name': 'Los Angeles', 'lat': 34.0522, 'lng': -118.2437},
    'california': {'name': 'California', 'lat': 36.7783, 'lng': -119.4179},
    'florida': {'name': 'Florida', 'lat': 27.6648, 'lng': -81.5158},
    'fl': {'name': 'Florida', 'lat': 27.6648, 'lng': -81.5158},
    'miami': {'name': 'Miami', 'lat': 25.7617, 'lng': -80.1918},
    'port of miami': {'name': 'PortMiami', 'lat': 25.7781, 'lng': -80.1794},
    'portmiami': {'name': 'PortMiami', 'lat': 25.7781, 'lng': -80.1794},
    'orlando': {'name': 'Orlando', 'lat': 28.5383, 'lng': -81.3792},
    'tampa': {'name': 'Tampa', 'lat': 27.9506, 'lng': -82.4572},
    'jacksonville': {'name': 'Jacksonville', 'lat': 30.3322, 'lng': -81.6557},
    'atlanta': {'name': 'Atlanta', 'lat': 33.7490, 'lng': -84.3880},
    'chicago': {'name': 'Chicago', 'lat': 41.8781, 'lng': -87.6298},
    'houston': {'name': 'Houston', 'lat': 29.7604, 'lng': -95.3698},
    'dallas': {'name': 'Dallas', 'lat': 32.7767, 'lng': -96.7970},
    'seattle': {'name': 'Seattle', 'lat': 47.6062, 'lng': -122.3321},
    'dubai airport': {'name': 'Dubai Airport', 'lat': 25.2532, 'lng': 55.3657},
    'dubai': {'name': 'Dubai Airport', 'lat': 25.2532, 'lng': 55.3657},
    'london heathrow': {'name': 'London Heathrow', 'lat': 51.4700, 'lng': -0.4543},
    'london': {'name': 'London Heathrow', 'lat': 51.4700, 'lng': -0.4543},
    'hamburg port': {'name': 'Hamburg Port', 'lat': 53.5511, 'lng': 9.9937},
    'hamburg': {'name': 'Hamburg Port', 'lat': 53.5511, 'lng': 9.9937},
    'new york': {'name': 'New York', 'lat': 40.7128, 'lng': -74.0060},
    'nyc': {'name': 'New York', 'lat': 40.7128, 'lng': -74.0060},
    'frankfurt': {'name': 'Frankfurt Rail Hub', 'lat': 50.1109, 'lng': 8.6821},
    'antwerp': {'name': 'Antwerp', 'lat': 51.2194, 'lng': 4.4025},
    'cologne': {'name': 'Cologne', 'lat': 50.9375, 'lng': 6.9603},
}

ROUTE_META = {
    'fastest': {
        'icon': '⚡',
        'label': 'Fastest',
        'speed_kmh': 78,
        'cost_per_km': 2.1,
        'carbon': 'Medium',
        'carbon_factor': 0.8,
        'color': '#3B82F6',
        'ai_suggestion': 'Uses the shortest available corridor and avoids high-delay transfer points.',
    },
    'lowest_cost': {
        'icon': '💰',
        'label': 'Lowest Cost',
        'speed_kmh': 58,
        'cost_per_km': 1.45,
        'carbon': 'Low',
        'carbon_factor': 0.65,
        'color': '#10B981',
        'ai_suggestion': 'Combines slower line-haul segments with lower carrier rates.',
    },
    'lowest_carbon': {
        'icon': '🌿',
        'label': 'Eco',
        'speed_kmh': 52,
        'cost_per_km': 1.75,
        'carbon': 'Very Low',
        'carbon_factor': 0.38,
        'color': '#4ADE80',
        'ai_suggestion': 'Prioritizes rail and consolidated handoffs to reduce emissions.',
    },
}


def location_for(value):
    key = normalize_location_key(value)
    if key in LOCATIONS:
        return LOCATIONS[key]
    if not key:
        raise ValueError('Location is required')
    if key in _geocode_cache:
        return _geocode_cache[key]

    response = requests.get(
        'https://nominatim.openstreetmap.org/search',
        params={'q': value, 'format': 'json', 'limit': 1},
        headers={'User-Agent': 'LogiSphere/1.0'},
        timeout=10,
    )
    response.raise_for_status()
    matches = response.json()
    if not matches:
        raise ValueError(f"Location not found: {value}")

    match = matches[0]
    location = {
        'name': match.get('display_name', value).split(',')[0],
        'lat': float(match['lat']),
        'lng': float(match['lon']),
    }
    _geocode_cache[key] = location
    return location


def normalize_location_key(value):
    key = str(value or '').strip().lower()
    key = re.sub(r'[^a-z0-9\s]', ' ', key)
    key = re.sub(r'\s+', ' ', key).strip()
    return key


def haversine_km(a, b):
    radius = 6371
    lat1, lng1, lat2, lng2 = map(radians, [a['lat'], a['lng'], b['lat'], b['lng']])
    delta_lat = lat2 - lat1
    delta_lng = lng2 - lng1
    h = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lng / 2) ** 2
    return 2 * radius * asin(sqrt(h))


def format_eta(hours):
    hours = max(1, round(hours))
    days, remaining_hours = divmod(hours, 24)
    if days:
        return f"{days}d {remaining_hours}h"
    return f"{remaining_hours}h"


def midpoint(a, b, offset=0):
    return {
        'lat': ((a['lat'] + b['lat']) / 2) + offset,
        'lng': ((a['lng'] + b['lng']) / 2) - offset,
    }


def coordinates_for(route_type, origin, destination):
    if route_type == 'fastest':
        via = midpoint(origin, destination, 0.25)
        return [[origin['lat'], origin['lng']], [via['lat'], via['lng']], [destination['lat'], destination['lng']]]

    if route_type == 'lowest_cost':
        via = midpoint(origin, destination, -0.35)
        return [[origin['lat'], origin['lng']], [via['lat'], via['lng']], [destination['lat'], destination['lng']]]

    if is_european(origin) and is_european(destination):
        frankfurt = LOCATIONS['frankfurt']
        return [[origin['lat'], origin['lng']], [frankfurt['lat'], frankfurt['lng']], [destination['lat'], destination['lng']]]

    via = midpoint(origin, destination, 0.65)
    return [[origin['lat'], origin['lng']], [via['lat'], via['lng']], [destination['lat'], destination['lng']]]


def is_european(location):
    return 35 <= location['lat'] <= 72 and -12 <= location['lng'] <= 35


def build_route(route_type, origin, destination):
    meta = ROUTE_META[route_type]
    distance = haversine_km(origin, destination)
    multiplier = {'fastest': 1.04, 'lowest_cost': 1.18, 'lowest_carbon': 1.28}[route_type]
    route_distance = distance * multiplier
    return {
        'id': route_type,
        'type': route_type,
        'origin': origin['name'],
        'destination': destination['name'],
        'icon': meta['icon'],
        'label': meta['label'],
        'eta': format_eta(route_distance / meta['speed_kmh']),
        'cost': round(route_distance * meta['cost_per_km']),
        'carbon': meta['carbon'],
        'carbon_kg': round(route_distance * meta['carbon_factor']),
        'color': meta['color'],
        'ai_suggestion': meta['ai_suggestion'],
        'coordinates': coordinates_for(route_type, origin, destination),
    }


def shipment_from_route(data, route):
    return {
        'tracking_number': data.get('tracking_number'),
        'origin': route['origin'],
        'destination': route['destination'],
        'carrier': data.get('carrier') or f"LogiSphere {route['label']}",
        'mode': data.get('mode') or 'Road',
        'status': data.get('status') or 'In Transit',
    }


@routes_bp.route('/optimize', methods=['GET', 'POST'])
def get_optimized_routes():
    data = request.get_json(silent=True) or request.args

    try:
        origin = location_for(data.get('origin') or 'Port of Rotterdam')
        destination = location_for(data.get('destination') or 'Munich Hub')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except requests.RequestException:
        return jsonify({'error': 'Unable to geocode that location right now. Please try a more specific city, port, or address.'}), 502

    routes = [build_route(route_type, origin, destination) for route_type in ROUTE_META]
    return jsonify({
        'origin': origin,
        'destination': destination,
        'routes': routes,
        'recommended': min(routes, key=lambda route: route['cost'] + route['carbon_kg']),
    }), 200
