"""
dtos/user_dto.py — Data Transfer Objects for User.

Classes:
  UserDTO       — outbound: model → JSON (camelCase), validated with Pydantic
  CreateUserDTO — inbound:  JSON → new model, validated with Pydantic
  UpdateUserDTO — inbound:  JSON → update existing model, validated with Pydantic
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

_VALID_ROLES = ('admin', 'user')


class UserDTO(BaseModel):
    """Outbound representation of a User (model → JSON)."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id:            int
    name:          str
    email:         str
    avatar:        str
    level:         int
    member_since:  str
    sessions:      int
    active:        bool
    role:          str
    main_asset_id: Optional[int] = None

    @classmethod
    def from_model(cls, user) -> dict:
        """Serialize a User ORM instance to a camelCase dict ready for jsonify."""
        return cls.model_validate(user).model_dump(by_alias=True)


class CreateUserDTO(BaseModel):
    """Inbound payload for creating a new user (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          str           = Field(min_length=1)
    email:         str
    password:      str           = Field(min_length=6)
    member_since:  str           = Field(min_length=1)
    avatar:        str           = '🧗'
    level:         int           = Field(default=0, ge=0)
    sessions:      int           = Field(default=0, ge=0)
    active:        bool          = True
    role:          str           = 'user'
    main_asset_id: Optional[int] = None

    @field_validator('email')
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('invalid email address')
        return v

    @field_validator('role')
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        if v not in _VALID_ROLES:
            raise ValueError(f"role must be one of: {', '.join(_VALID_ROLES)}")
        return v

    @classmethod
    def from_request(cls, data: dict) -> 'CreateUserDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)


class UpdateUserDTO(BaseModel):
    """Inbound payload for replacing an existing user (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          Optional[str]  = Field(default=None, min_length=1)
    email:         Optional[str]  = None
    member_since:  Optional[str]  = None
    avatar:        Optional[str]  = None
    level:         Optional[int]  = Field(default=None, ge=0)
    active:        Optional[bool] = None
    role:          Optional[str]  = None
    password:      Optional[str]  = Field(default=None, min_length=6)
    main_asset_id: Optional[int]  = None

    @field_validator('email')
    @classmethod
    def email_must_contain_at(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and '@' not in v:
            raise ValueError('invalid email address')
        return v

    @field_validator('role')
    @classmethod
    def role_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in _VALID_ROLES:
            raise ValueError(f"role must be one of: {', '.join(_VALID_ROLES)}")
        return v

    @classmethod
    def from_request(cls, data: dict) -> 'UpdateUserDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)
