"""
blueprints/auth.py — OAuth 2.0 token and revocation endpoints.

Routes:
  POST /api/v1/auth/token   → password grant or refresh_token grant
  POST /api/v1/auth/revoke  → revoke a refresh token
"""

from flask import Blueprint, jsonify, request

from ..auth.tokens import (
    ACCESS_TOKEN_EXPIRES,
    create_access_token,
    create_refresh_token,
    revoke_refresh_token,
    rotate_refresh_token,
)
from ..dtos.auth_dto import PasswordGrantDTO, RefreshGrantDTO, RevokeDTO, TokenResponseDTO
from ..models.users import User

auth_bp = Blueprint('auth', __name__)


def _oauth_error(error: str, description: str, status: int = 400):
    return jsonify({'error': error, 'error_description': description}), status


@auth_bp.route('/token', methods=['POST'])
def token():
    body = request.get_json(silent=True) or request.form.to_dict()

    grant_type = body.get('grant_type', '')

    if grant_type == 'password':
        dto = PasswordGrantDTO(**body)
        user = User.query.filter_by(email=dto.username).first()
        if user is None or not user.check_password(dto.password):
            return _oauth_error('invalid_grant', 'Invalid username or password', 401)

        access  = create_access_token(user)
        refresh = create_refresh_token(user)

    elif grant_type == 'refresh_token':
        dto = RefreshGrantDTO(**body)
        try:
            user, refresh = rotate_refresh_token(dto.refresh_token)
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


@auth_bp.route('/revoke', methods=['POST'])
def revoke():
    body = request.get_json(silent=True) or request.form.to_dict()
    dto = RevokeDTO(**body)
    revoke_refresh_token(dto.token)
    return jsonify({}), 200
