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

from typing import Optional

from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from ..auth.decorators import require_auth, require_role
from ..db import db
from ..models.users import User
from ..dtos.user_dto import UserDTO, CreateUserDTO, UpdateUserDTO
from .query_utils import apply_list_params
from .response_models import UserListResponse

_TAG = Tag(name='Users')
_SECURITY = [{"BearerAuth": []}]

users_bp = APIBlueprint('users', __name__, abp_tags=[_TAG])


class UserPath(BaseModel):
    user_id: int


class UserQuery(BaseModel):
    page:     Optional[int] = 1
    per_page: Optional[int] = 20
    sort:     Optional[str] = 'id'
    order:    Optional[str] = 'asc'
    name:     Optional[str] = None
    email:    Optional[str] = None
    role:     Optional[str] = None
    active:   Optional[str] = None


@users_bp.get('', responses={200: UserListResponse})
def get_all(query: UserQuery):
    """Return a paginated, filterable, sortable list of users."""
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


@users_bp.get('/<int:user_id>', responses={200: UserDTO})
def get_by_id(path: UserPath):
    """Return a single user identified by user_id."""
    user = User.query.get_or_404(path.user_id)
    return jsonify(UserDTO.from_model(user))


@users_bp.post('', security=_SECURITY, responses={201: UserDTO})
@require_auth
def create(body: CreateUserDTO):
    """Create and persist a new user from the request body."""
    user = User(
        name=body.name,
        email=body.email,
        avatar=body.avatar,
        level=body.level,
        member_since=body.member_since,
        sessions=body.sessions,
        active=body.active,
        role=body.role,
        main_asset_id=body.main_asset_id,
    )
    user.set_password(body.password)
    db.session.add(user)
    db.session.commit()
    return jsonify(UserDTO.from_model(user)), 201


@users_bp.put('/<int:user_id>', security=_SECURITY, responses={200: UserDTO})
@require_auth
def update(path: UserPath, body: UpdateUserDTO):
    """Replace fields of an existing user identified by user_id."""
    user = User.query.get_or_404(path.user_id)
    user.name          = body.name          or user.name
    user.email         = body.email         or user.email
    user.member_since  = body.member_since  or user.member_since
    user.avatar        = body.avatar        or user.avatar
    user.level         = body.level         if body.level  is not None else user.level
    user.active        = body.active        if body.active is not None else user.active
    user.role          = body.role          or user.role
    user.main_asset_id = body.main_asset_id if body.main_asset_id is not None else user.main_asset_id
    if body.password:
        user.set_password(body.password)
    db.session.commit()
    return jsonify(UserDTO.from_model(user))


@users_bp.delete('/<int:user_id>', security=_SECURITY, responses={204: None})
@require_role('admin')
def delete(path: UserPath):
    """Delete the user identified by user_id."""
    user = User.query.get_or_404(path.user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
