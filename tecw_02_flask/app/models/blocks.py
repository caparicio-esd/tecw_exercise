"""
models/blocks.py — Block ORM model.

Represents a bouldering problem (bloque) available at the gym.
"""

from ..db import db


class Block(db.Model):
    __tablename__ = "blocks"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    grade       = db.Column(db.String(10),  nullable=False)  # V-scale: V0, V3, V7, etc.
    color       = db.Column(db.String(7),   nullable=False)  # Hex colour code: #e74c3c
    sector      = db.Column(db.String(5),   nullable=False)
    height      = db.Column(db.Float,       nullable=False)  # metres
    city        = db.Column(db.String(50),  nullable=False)  # madrid / barcelona
    active      = db.Column(db.Boolean, default=True)
    picture     = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text,        nullable=True)

    def __repr__(self):
        return f"<Block {self.name} ({self.grade})>"
