"""
models/users.py — User ORM model.

Represents a gym member. Passwords are stored as bcrypt hashes via
werkzeug.security; plain-text passwords are never persisted.

Relationships:
  - assets (n--n via user_assets): all media files attached to this user.
  - main_asset_id: optional FK pointing to the profile picture asset.
"""

from werkzeug.security import generate_password_hash, check_password_hash

from ..db import db
from .associations import user_assets

user_roles = db.Enum('admin', 'user', name='user_roles')


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    avatar        = db.Column(db.String(10), default="🧗")
    level         = db.Column(db.Integer, nullable=False, default=0)  # 0=Principiante 1=Intermedio 2=Avanzado 3=Experto
    member_since  = db.Column(db.String(10), nullable=False)          # YYYY-MM-DD
    sessions      = db.Column(db.Integer, default=0)
    active        = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(255), nullable=False, server_default='')
    role          = db.Column(user_roles, default='user')
    main_asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)

    assets = db.relationship('Asset', secondary=user_assets, backref='users', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"

    def set_password(self, password):
        """Hash *password* and store it in password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if *password* matches the stored hash."""
        return check_password_hash(self.password_hash, password)
