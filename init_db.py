import os
from dotenv import load_dotenv
from app import create_app
from extensions import db
from models import Event, Newsletter

# Cargar entorno explícitamente
load_dotenv()

app = create_app()

with app.app_context():
    uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not uri:
        print("❌ ERROR: SQLALCHEMY_DATABASE_URI no encontrada en app.config")
        # Intentar ver si está en os.environ
        print(f"DATABASE_URL en os.environ: {'Definida' if os.getenv('DATABASE_URL') else 'NO Definida'}")
    else:
        print(f"Conectando a: ...@{uri.split('@')[-1] if '@' in uri else '???'}")
        print("Creando tablas en la base de datos...")
        try:
            db.create_all()
            print("✅ Tablas creadas exitosamente.")
        except Exception as e:
            print(f"❌ Error al crear tablas: {str(e)}")
