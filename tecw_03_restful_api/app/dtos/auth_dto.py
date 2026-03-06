"""
dtos/auth_dto.py — Auth DTOs (OAuth 2.0 uses snake_case, no camelCase alias).
"""

from pydantic import BaseModel


class PasswordGrantDTO(BaseModel):
    grant_type: str
    username: str
    password: str


class RefreshGrantDTO(BaseModel):
    grant_type: str
    refresh_token: str


class RevokeDTO(BaseModel):
    token: str


class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    expires_in: int
    refresh_token: str
