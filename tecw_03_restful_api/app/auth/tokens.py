"""
auth/tokens.py — JWT access tokens and opaque refresh token management.
"""

import secrets
from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app

from ..db import db
from ..models.refresh_tokens import RefreshToken

ACCESS_TOKEN_EXPIRES  = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRES = timedelta(days=30)


def create_access_token(user) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub':  str(user.id),
        'role': user.role,
        'iat':  now,
        'exp':  now + ACCESS_TOKEN_EXPIRES,
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def create_refresh_token(user) -> str:
    raw = secrets.token_urlsafe(64)
    rt = RefreshToken(
        token=raw,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRES,
    )
    db.session.add(rt)
    db.session.commit()
    return raw


def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT. Raises jwt.PyJWTError if invalid or expired."""
    return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])


def rotate_refresh_token(raw: str):
    """
    Validate *raw* refresh token, revoke it, and issue a new one.

    Returns (user, new_refresh_token_str) or raises ValueError on failure.
    """
    rt = RefreshToken.query.filter_by(token=raw, revoked=False).first()
    if rt is None:
        raise ValueError('invalid_grant')

    # Normalize: SQLite stores naive datetimes; compare against UTC naive
    expires_at = rt.expires_at
    now_utc = datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        now_cmp = datetime.utcnow()
    else:
        now_cmp = now_utc

    if expires_at < now_cmp:
        rt.revoked = True
        db.session.commit()
        raise ValueError('invalid_grant')

    user = rt.user
    rt.revoked = True
    db.session.commit()

    new_raw = create_refresh_token(user)
    return user, new_raw


def revoke_refresh_token(raw: str) -> bool:
    rt = RefreshToken.query.filter_by(token=raw, revoked=False).first()
    if rt is None:
        return False
    rt.revoked = True
    db.session.commit()
    return True
