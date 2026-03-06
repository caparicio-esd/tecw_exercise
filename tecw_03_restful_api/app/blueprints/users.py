"""
blueprints/users.py — User REST endpoints.

Base URL: /api/v1/users

Routes:
  GET    /            → list all users
  GET    /<id>        → get a single user by id
  POST   /            → create a new user
  PUT    /<id>        → replace an existing user
  DELETE /<id>        → delete a user
"""

from flask import Blueprint, jsonify, request

from ..db import db
from ..models.users import User
from ..dtos.user_dto import UserDTO, CreateUserDTO, UpdateUserDTO
from .query_utils import apply_list_params

users_bp = Blueprint('users', __name__)


@users_bp.route('')
def get_all():
    """Return a paginated, filterable, sortable list of users.

    Filters : name (like), email (like), role (exact), active (exact)
    Sort by : id (default), name, level, sessions, member_since
    """
    items, meta = apply_list_params(
        User,
        User.query,
        filterable={
            'name':   'like',
            'email':  'like',
            'role':   'exact',
            'active': 'exact',
        },
        sortable=['id', 'name', 'level', 'sessions', 'member_since'],
    )
    return jsonify({'data': [UserDTO.from_model(u) for u in items], 'pagination': meta})


@users_bp.route('/<int:user_id>')
def get_by_id(user_id):
    """Return a single user identified by *user_id*."""
    user = User.query.get_or_404(user_id)
    return jsonify(UserDTO.from_model(user))


@users_bp.route('', methods=['POST'])
def create():
    """Create and persist a new user from the request body."""
    dto = CreateUserDTO.from_request(request.get_json())
    user = User(
        name=dto.name,
        email=dto.email,
        avatar=dto.avatar,
        level=dto.level,
        member_since=dto.member_since,
        sessions=dto.sessions,
        active=dto.active,
        role=dto.role,
        main_asset_id=dto.main_asset_id,
    )
    user.set_password(dto.password)
    db.session.add(user)
    db.session.commit()
    return jsonify(UserDTO.from_model(user)), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    """Replace all fields of an existing user identified by *user_id*."""
    user = User.query.get_or_404(user_id)
    dto = UpdateUserDTO.from_request(request.get_json())
    user.name          = dto.name          or user.nameque
    user.email         = dto.email         or user.email
    user.member_since  = dto.member_since  or user.member_since
    user.avatar        = dto.avatar        or user.avatar
    user.level         = dto.level         if dto.level  is not None else user.level
    user.active        = dto.active        if dto.active is not None else user.active
    user.role          = dto.role          or user.role
    user.main_asset_id = dto.main_asset_id if dto.main_asset_id is not None else user.main_asset_id
    if dto.password:
        user.set_password(dto.password)
    db.session.commit()
    return jsonify(UserDTO.from_model(user))


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    """Delete the user identified by *user_id*."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
