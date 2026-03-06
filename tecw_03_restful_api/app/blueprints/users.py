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

users_bp = Blueprint('users', __name__)


@users_bp.route('')
def get_all():
    """Return a list of all users."""
    users = User.query.all()
    return jsonify([_serialize(u) for u in users])


@users_bp.route('/<int:user_id>')
def get_by_id(user_id):
    """Return a single user identified by *user_id*."""
    user = User.query.get_or_404(user_id)
    return jsonify(_serialize(user))


@users_bp.route('', methods=['POST'])
def create():
    """Create and persist a new user from the request body."""
    data = request.get_json()
    user = User(
        name=data['name'],
        email=data['email'],
        avatar=data.get('avatar', '🧗'),
        level=data.get('level', 0),
        member_since=data['member_since'],
        sessions=data.get('sessions', 0),
        active=data.get('active', True),
        role=data.get('role', 'user'),
        main_asset_id=data.get('main_asset_id'),
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(_serialize(user)), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    """Replace all fields of an existing user identified by *user_id*."""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name          = data['name']
    user.email         = data['email']
    user.avatar        = data.get('avatar', user.avatar)
    user.level         = data.get('level', user.level)
    user.member_since  = data['member_since']
    user.active        = data.get('active', user.active)
    user.role          = data.get('role', user.role)
    user.main_asset_id = data.get('main_asset_id', user.main_asset_id)
    if data.get('password'):
        user.set_password(data['password'])
    db.session.commit()
    return jsonify(_serialize(user))


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    """Delete the user identified by *user_id*."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


def _serialize(user):
    return {
        'id':            user.id,
        'name':          user.name,
        'email':         user.email,
        'avatar':        user.avatar,
        'level':         user.level,
        'member_since':  user.member_since,
        'sessions':      user.sessions,
        'active':        user.active,
        'role':          user.role,
        'main_asset_id': user.main_asset_id,
    }
