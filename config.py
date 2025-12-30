import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Configuración base de la aplicación."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_default')
    
    # Obtener y limpiar DATABASE_URL
    raw_db_url = os.getenv('DATABASE_URL', '')
    
    # Limpiar comillas accidentales y espacios
    _db_url = raw_db_url.strip().strip("'").strip("\"")
    
    if not _db_url:
        logger.warning("DATABASE_URL no está definida o está vacía.")
        SQLALCHEMY_DATABASE_URI = None
    else:
        # Corregir prefijo para SQLAlchemy 1.4+
        if _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        
        SQLALCHEMY_DATABASE_URI = _db_url
        
        # Log de seguridad (solo muestra el host)
        _safe_url = _db_url.split('@')[-1] if '@' in _db_url else "URL oculta"
        logger.info(f"SQLALCHEMY_DATABASE_URI configurada: ...@{_safe_url}")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # Rate Limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URI = "memory://"
