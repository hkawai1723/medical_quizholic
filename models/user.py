from datetime import datetime, timezone

from argon2 import PasswordHasher
from flask_login import UserMixin

from extensions import db

ph = PasswordHasher()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    _password_hash = db.Column('password_hash', db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    latest_login = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    auth_provider = db.Column(db.String(20), default='local')  # 'local' or 'google'


    def set_password(self, password):
        self._password_hash = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self._password_hash, password)
        except:
            return False

    def change_password(self, new_password):
        self.set_password(new_password)
        db.session.commit()

    def __str__(self):
        return f'{self.name}, {self.email}'

    def __repr__(self):
        return f'<Name {self.name}>'
