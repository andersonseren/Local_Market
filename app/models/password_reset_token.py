from app.extensions import db
from datetime import datetime, timedelta
import secrets

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='reset_tokens')
    
    @classmethod
    def create_token(cls, user):
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        reset_token = cls(user_id=user.id, token=token, expires_at=expires_at)
        db.session.add(reset_token)
        db.session.commit()
        return token
    
    @classmethod
    def validate_token(cls, token):
        reset_token = cls.query.filter_by(token=token, used=False).first()
        if not reset_token:
            return None
        if reset_token.expires_at < datetime.utcnow():
            return None
        return reset_token
    
    def mark_used(self):
        self.used = True
        db.session.commit()