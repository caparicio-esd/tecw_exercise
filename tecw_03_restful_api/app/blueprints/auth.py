"""
blueprints/auth.py — OAuth 2.0 token and revocation endpoints.

Routes:
  POST /api/v1/auth/token   → password grant or refresh_token grant
  POST /api/v1/auth/revoke  → revoke a refresh token
"""

from typing import Optional

from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from ..auth.tokens import (
    ACCESS_TOKEN_EXPIRES,
    create_access_token,
    create_refresh_token,
    revoke_refresh_token,
    rotate_refresh_token,
)
from ..dtos.auth_dto import RevokeDTO, TokenResponseDTO
from pydantic import BaseModel as _BaseModel

class _Empty(_BaseModel):
    pass
from ..models.users import User

_TAG = Tag(name='Auth')

auth_bp = APIBlueprint('auth', __name__, abp_tags=[_TAG])


def _oauth_error(error: str, description: str, status: int = 400):
    return jsonify({'error': error, 'error_description': description}), status


class TokenRequestBody(BaseModel):
    """Flexible body for /token — covers both password grant and refresh_token grant."""
    grant_type:    str
    username:      Optional[str] = None
    password:      Optional[str] = None
    refresh_token: Optional[str] = None


@auth_bp.post('/token', responses={200: TokenResponseDTO})
def token(body: TokenRequestBody):
    """Issue an access token (password grant or refresh_token grant)."""
    grant_type = body.grant_type

    if grant_type == 'password':
        user = User.query.filter_by(email=body.username).first()
        if user is None or not user.check_password(body.password):
            return _oauth_error('invalid_grant', 'Invalid username or password', 401)

        access  = create_access_token(user)
        refresh = create_refresh_token(user)

    elif grant_type == 'refresh_token':
        if not body.refresh_token:
            return _oauth_error('invalid_request', 'refresh_token is required')
        try:
            user, refresh = rotate_refresh_token(body.refresh_token)
        except ValueError:
            return _oauth_error('invalid_grant', 'Refresh token is invalid or expired', 401)
        access = create_access_token(user)

    else:
        return _oauth_error('unsupported_grant_type', f'Grant type "{grant_type}" is not supported')

    response = TokenResponseDTO(
        access_token=access,
        expires_in=int(ACCESS_TOKEN_EXPIRES.total_seconds()),
        refresh_token=refresh,
    )
    return jsonify(response.model_dump()), 200


@auth_bp.post('/revoke', responses={200: _Empty})
def revoke(body: RevokeDTO):
    """Revoke a refresh token."""
    revoke_refresh_token(body.token)
    return jsonify({}), 200
