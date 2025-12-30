from flask import Blueprint, jsonify, request
from datetime import datetime
from extensions import db
from models import Event, Newsletter

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

def api_response(status, data=None, message=None, code=200):
    """Helper para estandarizar respuestas JSON."""
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    return jsonify(response), code

@api_bp.route('/stats', methods=['GET'])
def health_check():
    """Endpoint de estado para health checks."""
    try:
        # Prueba simple de conexión a DB
        db.session.execute(db.text('SELECT 1'))
        return api_response(
            status="ok",
            data={
                "database": "connected",
                "db_host": db_host,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        return api_response(
            status="error", 
            message=f"System check failed: {str(e)}", 
            code=500
        )

@api_bp.route('/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """Obtiene eventos futuros con status 'finalizado'."""
    try:
        now = datetime.utcnow()
        events = Event.query.filter(
            Event.status == 'finalizado',
            Event.event_date >= now
        ).order_by(Event.event_date.asc()).all()

        return api_response(
            status="success",
            data=[e.to_dict() for e in events]
        )
    except Exception as e:
        return api_response(
            status="error",
            message=f"Error retrieving events: {str(e)}",
            code=500
        )

@api_bp.route('/newsletters', methods=['GET'])
def get_newsletters():
    """Obtiene listado paginado de newsletters publicados."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Validación básica de inputs
        if page < 1: page = 1
        if per_page < 1 or per_page > 50: per_page = 10

        pagination = Newsletter.query.filter_by(is_published=True)\
            .order_by(Newsletter.published_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return api_response(
            status="success",
            data={
                "items": [n.to_dict() for n in pagination.items],
                "total": pagination.total,
                "pages": pagination.pages,
                "current_page": page
            }
        )
    except Exception as e:
        return api_response(
            status="error",
            message=f"Error retrieving newsletters: {str(e)}",
            code=500
        )

@api_bp.route('/newsletters/<int:id>', methods=['GET'])
def get_newsletter_detail(id):
    """Obtiene el detalle (HTML) de un newsletter específico."""
    try:
        if id < 1:
            return api_response(status="error", message="Invalid ID", code=400)

        newsletter = Newsletter.query.get(id)
        
        if not newsletter or not newsletter.is_published:
            return api_response(status="error", message="Newsletter not found", code=404)

        return api_response(
            status="success",
            data=newsletter.to_dict(include_html=True)
        )
    except Exception as e:
        return api_response(
            status="error",
            message=f"Error retrieving newsletter: {str(e)}",
            code=500
        )
