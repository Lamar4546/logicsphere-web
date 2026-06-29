from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def get_dashboard():
    # Will be replaced with real Supabase queries later
    return jsonify({
        'kpis': {
            'active_shipments': 1248,
            'at_risk_delays': 14,
            'customs_exceptions': 3,
            'ai_cost_savings': 42150
        },
        'alerts': [
            {
                'type': 'severe',
                'title': 'SEVERE DELAY HAZARD',
                'message': "Vessel 'Ever-Cloud' arriving 8h late due to weather anomaly."
            },
            {
                'type': 'warning',
                'title': 'FUEL OPPORTUNITY',
                'message': 'Lower speed for Fleet-34 will reduce consumption.'
            }
        ]
    }), 200