"""
models/refresh_tokens.py — RefreshToken ORM model.

Stores opaque refresh tokens linked to users.
Tokens are rotated on each use and expire after 30 days.
"""

from ..db import db


class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'

    id         = db.Column(db.Integer, primary_key=True)
    token      = db.Column(db.String(86), unique=True, nullable=False, index=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked    = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship('User', backref='refresh_tokens')
