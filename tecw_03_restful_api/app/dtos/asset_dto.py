"""
dtos/asset_dto.py — Data Transfer Objects for Asset.

Classes:
  AssetDTO       — outbound: model → JSON (camelCase), validated with Pydantic
  CreateAssetDTO — inbound:  JSON → new model, validated with Pydantic
"""

from pydantic import BaseModel, ConfigDict, AnyHttpUrl, field_validator
from pydantic.alias_generators import to_camel


class AssetDTO(BaseModel):
    """Outbound representation of an Asset (model → JSON)."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id:  int
    url: str

    @classmethod
    def from_model(cls, asset) -> dict:
        """Serialize an Asset ORM instance to a camelCase dict ready for jsonify."""
        return cls.model_validate(asset).model_dump(by_alias=True)


class CreateAssetDTO(BaseModel):
    """Inbound payload for registering a new asset (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    url: AnyHttpUrl

    @field_validator('url', mode='after')
    @classmethod
    def url_to_str(cls, v: AnyHttpUrl) -> str:
        """Normalize the validated URL back to a plain string for the ORM."""
        return str(v)

    @classmethod
    def from_request(cls, data: dict) -> 'CreateAssetDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)
