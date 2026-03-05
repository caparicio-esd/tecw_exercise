from ..db import db


class Way(db.Model):
    __tablename__ = "ways"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    grade       = db.Column(db.String(10), nullable=False)   # Escala francesa: 6a, 7b+, etc.
    type        = db.Column(db.String(20), nullable=False)   # Deportiva / Top-rope / Boulder
    length      = db.Column(db.Integer, nullable=False)      # metros
    city        = db.Column(db.String(50), nullable=False)   # madrid / barcelona
    active      = db.Column(db.Boolean, default=True)
    picture     = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Way {self.name} ({self.grade})>"
