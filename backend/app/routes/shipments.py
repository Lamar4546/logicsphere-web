from datetime import datetime, timedelta, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request
from supabase import create_client

from ..config import Config

shipments_bp = Blueprint('shipments', __name__)

_supabase = None
_memory_shipments = [
    {
        'id': 'demo-1',
        'tracking_number': 'LS-2024-001',
        'origin': 'Port of Rotterdam',
        'destination': 'Munich Hub',
        'status': 'In Transit',
        'carrier': 'Maersk',
        'mode': 'Ocean',
        'eta': (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
    },
    {
        'id': 'demo-2',
        'tracking_number': 'LS-2024-002',
        'origin': 'Shanghai Port',
        'destination': 'Los Angeles',
        'status': 'Delayed',
        'carrier': 'COSCO',
        'mode': 'Ocean',
        'eta': (datetime.now(timezone.utc) + timedelta(days=5)).isoformat(),
    },
    {
        'id': 'demo-3',
        'tracking_number': 'LS-2024-003',
        'origin': 'Dubai Airport',
        'destination': 'London Heathrow',
        'status': 'In Transit',
        'carrier': 'Emirates Cargo',
        'mode': 'Air',
        'eta': (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    },
    {
        'id': 'demo-4',
        'tracking_number': 'LS-2024-004',
        'origin': 'Hamburg Port',
        'destination': 'New York',
        'status': 'At Customs',
        'carrier': 'MSC',
        'mode': 'Ocean',
        'eta': (datetime.now(timezone.utc) + timedelta(days=3)).isoformat(),
    },
]


def get_supabase():
    global _supabase
    if _supabase is None and Config.SUPABASE_URL and Config.SUPABASE_KEY:
        _supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    return _supabase


def normalize_shipment(data):
    data = data or {}
    required = ['tracking_number', 'origin', 'destination']
    missing = [field for field in required if not str(data.get(field, '')).strip()]
    if missing:
        return None, f"Missing required field(s): {', '.join(missing)}"

    eta = data.get('eta') or (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    return {
        'tracking_number': str(data.get('tracking_number')).strip(),
        'origin': str(data.get('origin')).strip(),
        'destination': str(data.get('destination')).strip(),
        'carrier': str(data.get('carrier') or 'Unassigned').strip(),
        'mode': str(data.get('mode') or 'Ocean').strip(),
        'status': str(data.get('status') or 'In Transit').strip(),
        'eta': eta,
    }, None


def is_archived(shipment):
    return shipment.get('archived') is True or str(shipment.get('status', '')).lower() == 'archived'


@shipments_bp.route('/', methods=['GET'])
def get_shipments():
    try:
        supabase = get_supabase()
        if supabase:
            res = supabase.table('shipments').select('*').order('created_at', desc=True).execute()
            shipments = res.data or []
            if request.args.get('include_archived') != 'true':
                shipments = [shipment for shipment in shipments if not is_archived(shipment)]
            return jsonify(shipments), 200
    except Exception:
        pass

    shipments = _memory_shipments
    if request.args.get('include_archived') != 'true':
        shipments = [shipment for shipment in shipments if not is_archived(shipment)]
    return jsonify(shipments), 200


@shipments_bp.route('/<shipment_id>', methods=['GET'])
def get_shipment(shipment_id):
    try:
        supabase = get_supabase()
        if supabase:
            res = supabase.table('shipments').select('*').eq('id', shipment_id).single().execute()
            return jsonify(res.data), 200
    except Exception:
        pass

    shipment = next((s for s in _memory_shipments if str(s['id']) == shipment_id), None)
    if not shipment:
        return jsonify({'error': 'Shipment not found'}), 404
    return jsonify(shipment), 200


@shipments_bp.route('/', methods=['POST'])
def create_shipment():
    shipment, error = normalize_shipment(request.get_json())
    if error:
        return jsonify({'error': error}), 400

    try:
        supabase = get_supabase()
        if supabase:
            res = supabase.table('shipments').insert(shipment).execute()
            created = res.data[0] if res.data else shipment
            return jsonify(created), 201
    except Exception:
        pass

    created = {'id': str(uuid4()), **shipment}
    _memory_shipments.append(created)
    return jsonify(created), 201


@shipments_bp.route('/<shipment_id>', methods=['PATCH'])
def update_shipment(shipment_id):
    updates = request.get_json() or {}
    allowed = {'tracking_number', 'origin', 'destination', 'carrier', 'mode', 'status', 'eta', 'archived'}
    updates = {key: value for key, value in updates.items() if key in allowed}
    if not updates:
        return jsonify({'error': 'No valid updates supplied'}), 400

    try:
        supabase = get_supabase()
        if supabase:
            res = supabase.table('shipments').update(updates).eq('id', shipment_id).execute()
            updated = res.data[0] if res.data else {'id': shipment_id, **updates}
            return jsonify(updated), 200
    except Exception:
        pass

    for shipment in _memory_shipments:
        if str(shipment['id']) == shipment_id:
            shipment.update(updates)
            return jsonify(shipment), 200
    return jsonify({'error': 'Shipment not found'}), 404


@shipments_bp.route('/<shipment_id>/archive', methods=['POST'])
def archive_shipment(shipment_id):
    updates = {'archived': True, 'status': 'Archived'}

    try:
        supabase = get_supabase()
        if supabase:
            try:
                res = supabase.table('shipments').update(updates).eq('id', shipment_id).execute()
            except Exception:
                res = supabase.table('shipments').update({'status': 'Archived'}).eq('id', shipment_id).execute()
            archived = res.data[0] if res.data else {'id': shipment_id, **updates}
            return jsonify(archived), 200
    except Exception:
        pass

    for shipment in _memory_shipments:
        if str(shipment['id']) == shipment_id:
            shipment.update(updates)
            return jsonify(shipment), 200
    return jsonify({'error': 'Shipment not found'}), 404


@shipments_bp.route('/<shipment_id>', methods=['DELETE'])
def delete_shipment(shipment_id):
    try:
        supabase = get_supabase()
        if supabase:
            supabase.table('shipments').delete().eq('id', shipment_id).execute()
            return jsonify({'message': 'Shipment removed'}), 200
    except Exception:
        pass

    before = len(_memory_shipments)
    _memory_shipments[:] = [s for s in _memory_shipments if str(s['id']) != shipment_id]
    if len(_memory_shipments) == before:
        return jsonify({'error': 'Shipment not found'}), 404
    return jsonify({'message': 'Shipment removed'}), 200
