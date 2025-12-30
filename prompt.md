Necesito que generes monroe-backend-api DESDE CERO con:

ARCHIVOS:
1. app.py (Application Factory - Flask)
2. config.py (Configuración + env vars)
3. extensions.py (Inicialización db, limiter, cors)
4. models.py (ORM - Event, Newsletter)
5. routes/__init__.py
6. routes/api_routes.py (4 endpoints GET)
7. requirements.txt
8. .env.example
9. .gitignore

ENDPOINTS (READ-ONLY):
- GET /api/v1/events/upcoming → eventos finalizados (status='finalizado')
- GET /api/v1/newsletters → listado paginado (is_published=true)
- GET /api/v1/newsletters/<id> → newsletter específico
- GET /api/v1/stats → health check

REGLAS:
✅ Responsabilidad única: app.py=factory, config.py=vars, extensions.py=init, models.py=ORM, routes=endpoints
✅ Máx 300 líneas archivo, 40 líneas función
✅ Nombres descriptivos (get_upcoming_events, not get_data)
✅ Error handling: {"status": "success|error", "data": ..., "message": ...}
✅ Validación de inputs (tipo, rango, existencia)
✅ CORS: ["http://localhost:3000", "https://meetmonroe.us"]
✅ Rate limiting: 100 req/min por IP
✅ Sin autenticación (datos públicos)
✅ SQLAlchemy ORM (sin raw SQL)

DESPUÉS:
1. Genera todos los archivos en la carpeta actual
2. Instala dependencias: pip install -r requirements.txt
3. Crea .env desde .env.example
4. Prueba: flask run
5. Valida endpoints: curl http://localhost:5000/api/v1/stats

¿Puedes hacerlo todo?