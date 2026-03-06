"""
auth/decorators.py — @require_auth and @require_role decorators.
"""

from functools import wraps

import jwt
from flask import abort, g, request

from .tokens import decode_access_token


def require_auth(f):
    """Verify Bearer JWT; store payload in flask.g.token_payload."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            abort(401)
        token = auth_header[len('Bearer '):]
        try:
            g.token_payload = decode_access_token(token)
        except jwt.PyJWTError:
            abort(401)
        return f(*args, **kwargs)
    return decorated


def require_role(role: str):
    """Decorator factory: require_auth + role check."""
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated(*args, **kwargs):
            if g.token_payload.get('role') != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator
