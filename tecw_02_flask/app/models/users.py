from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash

from ..db import db


class User(db.Model):
    __tablename__ = "users"

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    avatar       = db.Column(db.String(10), default="🧗")
    level        = db.Column(db.String(20), nullable=False)  # Principiante / Intermedio / Avanzado / Experto
    city         = db.Column(db.String(50), nullable=False)
    member_since = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    sessions     = db.Column(db.Integer, default=0)
    active       = db.Column(db.Boolean, default=True)
    picture      = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False, server_default='')
    role = db.Column(Enum('admin', 'user', name='user_roles'), default='user')


    def __repr__(self):
        return f"<User {self.name}>"

    def set_password(self, password):
        """Genera el hash de la contraseña y lo almacena."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña ingresada es correcta."""
        return check_password_hash(self.password_hash, password)
