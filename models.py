from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Link(db.Model):
    __tablename__ = 'links'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    url = db.Column(db.Text, nullable=False)
    mode = db.Column(db.String(10), nullable=False, default='xd')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    click_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Link {self.code}: {self.url}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'url': self.url,
            'mode': self.mode,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'click_count': self.click_count
        }