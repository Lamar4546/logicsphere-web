from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    jwt.init_app(app)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.shipments import shipments_bp
    from .routes.routes_module import routes_bp
    from .routes.ai_assistant import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(shipments_bp, url_prefix='/api/shipments')
    app.register_blueprint(routes_bp, url_prefix='/api/routes')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    @app.route('/api/health')
    def health():
        return {'status': 'LogiSphere API running'}, 200

    return app
