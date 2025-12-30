import os
from dotenv import load_dotenv
from app import create_app
from extensions import db
from models import Event, Newsletter
from datetime import datetime, timedelta


# Cargar entorno explícitamente
load_dotenv()


app = create_app()


with app.app_context():
    uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not uri:
        print("❌ ERROR: SQLALCHEMY_DATABASE_URI no encontrada en app.config")
        print(f"DATABASE_URL en os.environ: {'Definida' if os.getenv('DATABASE_URL') else 'NO Definida'}")
    else:
        print(f"Conectando a: ...@{uri.split('@')[-1] if '@' in uri else '???'}")
        print("Creando tablas en la base de datos...")
        try:
            db.create_all()
            print("✅ Tablas creadas exitosamente.")
            
            # Verificar si hay newsletters
            newsletter_count = db.session.query(Newsletter).count()
            
            if newsletter_count == 0:
                print("📝 Insertando datos de prueba...")
                
                # Newsletter 1
                newsletter1 = Newsletter(
                    title="Monroe Events - Week of January 1, 2025",
                    content_html="""
                    <h1>Welcome to Monroe Newsletter</h1>
                    <p>This week's top events in Monroe, Louisiana:</p>
                    <ul>
                        <li>New Year's Celebration at Civic Center</li>
                        <li>Winter Farmers Market</li>
                        <li>Live Music at Enoch's</li>
                    </ul>
                    """,
                    is_published=True,
                    published_at=datetime.utcnow() - timedelta(days=7)
                )
                
                # Newsletter 2
                newsletter2 = Newsletter(
                    title="Monroe Events - Week of December 25, 2024",
                    content_html="""
                    <h1>Holiday Events in Monroe</h1>
                    <p>Celebrate the season with these local events:</p>
                    <ul>
                        <li>Christmas Market Downtown</li>
                        <li>Holiday Lights Tour</li>
                        <li>Community Caroling Night</li>
                    </ul>
                    """,
                    is_published=True,
                    published_at=datetime.utcnow() - timedelta(days=14)
                )
                
                # Newsletter 3
                newsletter3 = Newsletter(
                    title="Monroe Events - Week of December 18, 2024",
                    content_html="""
                    <h1>Pre-Holiday Events</h1>
                    <p>Don't miss these events before the holidays:</p>
                    <ul>
                        <li>Local Art Gallery Opening</li>
                        <li>Community Potluck Dinner</li>
                        <li>Free Movie Night at the Park</li>
                    </ul>
                    """,
                    is_published=True,
                    published_at=datetime.utcnow() - timedelta(days=21)
                )
                
                db.session.add_all([newsletter1, newsletter2, newsletter3])
                db.session.commit()
                print("✅ 3 newsletters de prueba insertadas.")
            else:
                print(f"ℹ️  Ya existen {newsletter_count} newsletter(s) en la base de datos.")
                
        except Exception as e:
            print(f"❌ Error al crear tablas: {str(e)}")
            db.session.rollback()
