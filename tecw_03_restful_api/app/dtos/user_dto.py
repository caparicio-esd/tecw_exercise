"""
dtos/user_dto.py — Data Transfer Objects for User.

Defines how a User is serialized to JSON (output) and how incoming
request bodies are validated and parsed (input), keeping that logic
out of the blueprint and the model.

Classes:
  UserDTO       — outbound: model → JSON
  CreateUserDTO — inbound:  JSON → new model
  UpdateUserDTO — inbound:  JSON → update existing model
"""

from dataclasses import dataclass
from typing import Optional


def to_camel(snake: str) -> str:
    """Convert a snake_case string to camelCase."""
    parts = snake.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])


def camelize(d: dict) -> dict:
    """Return a new dict with all keys converted from snake_case to camelCase."""
    return {to_camel(k): v for k, v in d.items()}


@dataclass
class UserDTO:
    """Outbound representation of a User (model → JSON)."""

    id:            int
    name:          str
    email:         str
    avatar:        str
    level:         int
    member_since:  str
    sessions:      int
    active:        bool
    role:          str
    main_asset_id: Optional[int]

    @staticmethod
    def from_model(user) -> dict:
        """Serialize a User ORM instance to a camelCase dict ready for jsonify."""
        return camelize({
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
        })


@dataclass
class CreateUserDTO:
    """Inbound payload for creating a new user (JSON → model)."""

    name:          str
    email:         str
    password:      str
    member_since:  str
    avatar:        str           = '🧗'
    level:         int           = 0
    sessions:      int           = 0
    active:        bool          = True
    role:          str           = 'user'
    main_asset_id: Optional[int] = None

    @staticmethod
    def from_request(data: dict) -> 'CreateUserDTO':
        """
        Parse a request body dict into a CreateUserDTO.
        Raises KeyError if a required field is missing.
        """
        return CreateUserDTO(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            member_since=data['member_since'],
            avatar=data.get('avatar', '🧗'),
            level=data.get('level', 0),
            sessions=data.get('sessions', 0),
            active=data.get('active', True),
            role=data.get('role', 'user'),
            main_asset_id=data.get('main_asset_id'),
        )


@dataclass
class UpdateUserDTO:
    """Inbound payload for replacing an existing user (JSON → model)."""

    name:          Optional[str]  = None
    email:         Optional[str]  = None
    member_since:  Optional[str]  = None
    avatar:        Optional[str]  = None
    level:         Optional[int]  = None
    active:        Optional[bool] = None
    role:          Optional[str]  = None
    password:      Optional[str]  = None
    main_asset_id: Optional[int]  = None

    @staticmethod
    def from_request(data: dict) -> 'UpdateUserDTO':
        """
        Parse a request body dict into an UpdateUserDTO.
        Raises KeyError if a required field is missing.
        """
        return UpdateUserDTO(
            name=data.get('name'),
            email=data.get('email'),
            member_since=data.get('member_since'),
            avatar=data.get('avatar'),
            level=data.get('level'),
            active=data.get('active'),
            role=data.get('role'),
            password=data.get('password'),
            main_asset_id=data.get('main_asset_id'),
        )
