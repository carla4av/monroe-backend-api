from flask import Flask, jsonify
from config import Config
from extensions import db, cors, limiter
from routes import api_bp

def create_app(config_class=Config):
    """Factory function para crear la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    limiter.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(api_bp)

    # Manejadores de errores globales
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"status": "error", "message": "Rate limit exceeded"}), 429

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
