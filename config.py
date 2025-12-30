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
    
    # Manejo de DATABASE_URL para compatibilidad con SQLAlchemy 1.4+
    _db_url = os.getenv('DATABASE_URL')
    
    if not _db_url:
        logger.warning("DATABASE_URL no está definida en el entorno.")
        SQLALCHEMY_DATABASE_URI = None
    else:
        if _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        
        # Ocultar password en logs para seguridad
        _safe_url = _db_url.split('@')[-1] if '@' in _db_url else "URL malformada"
        logger.info(f"Base de datos configurada hacia: ...@{_safe_url}")
        SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # Rate Limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URI = "memory://"
