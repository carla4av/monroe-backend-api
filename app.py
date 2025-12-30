from flask import Flask, jsonify
from config import Config
from extensions import db, cors, limiter
from routes import api_bp
import logging

def create_app(config_class=Config):
    """Factory function para crear la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Verificar configuración crítica
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        app.logger.error("ERROR CRÍTICO: SQLALCHEMY_DATABASE_URI no configurada.")

    # Inicializar extensiones
    try:
        db.init_app(app)
    except Exception as e:
        app.logger.error(f"Error al inicializar la base de datos: {str(e)}")

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

# Instancia global para Gunicorn (app:app)
app = create_app()

if __name__ == '__main__':
    # Esto solo se ejecuta localmente con `python app.py`
    app.run(host='0.0.0.0', port=5000)
