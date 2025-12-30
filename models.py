from datetime import datetime
from extensions import db

class Event(db.Model):
    """Modelo para eventos (tabla 'events')."""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    final_description = db.Column(db.Text)
    event_date = db.Column(db.DateTime)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    link = db.Column(db.String(500))
    status = db.Column(db.String(50))  # pending_revision, aprobado, finalizado...
    is_highlight = db.Column(db.Boolean, default=False)
    group_title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "date": self.event_date.isoformat() if self.event_date else None,
            "category": self.category,
            "description": self.final_description or self.description,
            "image_url": self.image_url,
            "link": self.link,
            "is_highlight": self.is_highlight
        }

class Newsletter(db.Model):
    """Modelo para newsletters (tabla 'newsletters')."""
    __tablename__ = 'newsletters'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    content_html = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_html=False):
        """Convierte el objeto a diccionario."""
        data = {
            "id": self.id,
            "subject": self.subject,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "url": f"/api/v1/newsletters/{self.id}"
        }
        if include_html:
            data["content_html"] = self.content_html
            data["created_at"] = self.created_at.isoformat() if self.created_at else None
        return data
