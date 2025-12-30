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
    
    # Obtener DATABASE_URL
    raw_db_url = os.getenv('DATABASE_URL', '')
    
    # Limpieza profunda de comillas y espacios
    _db_url = raw_db_url.strip()
    # Eliminar comillas si están envolviendo la cadena
    if (_db_url.startswith("'") and _db_url.endswith("'")) or \
       (_db_url.startswith("\"") and _db_url.endswith("\"")):
        _db_url = _db_url[1:-1].strip()
    else:
        # Por si solo hay una al final o al inicio
        _db_url = _db_url.strip("'").strip("\"").strip()
    
    if not _db_url:
        logger.warning("DATABASE_URL no está definida o está vacía.")
        SQLALCHEMY_DATABASE_URI = None
    else:
        # Ajuste para psycopg 3 (v3 requiere postgresql+psycopg://)
        if _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql+psycopg://", 1)
        elif _db_url.startswith("postgresql://"):
            _db_url = _db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        
        SQLALCHEMY_DATABASE_URI = _db_url
        
        # Log de seguridad
        _safe_url = _db_url.split('@')[-1] if '@' in _db_url else "URL oculta"
        logger.info(f"SQLALCHEMY_DATABASE_URI configurada: ...@{_safe_url}")


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')


    # Rate Limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URI = "memory://"
