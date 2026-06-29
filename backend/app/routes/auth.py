from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from supabase import create_client
from ..config import Config

auth_bp = Blueprint('auth', __name__)

def get_supabase():
    missing = Config.missing_supabase_settings()
    if missing:
        raise RuntimeError(f"Missing Supabase configuration: {', '.join(missing)}")
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    try:
        supabase = get_supabase()

        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        user = getattr(res, "user", None)

        return jsonify({
            'message': 'Registration successful',
            'email': getattr(user, "email", None)
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    try:
        supabase = get_supabase()

        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        token = create_access_token(identity=res.user.id)

        return jsonify({
            'token': token,
            'email': res.user.email
        }), 200

    except Exception:
        return jsonify({'error': 'Invalid credentials'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out'}), 200
