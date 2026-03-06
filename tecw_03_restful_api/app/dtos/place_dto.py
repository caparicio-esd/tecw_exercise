"""
dtos/place_dto.py — Data Transfer Objects for Place.

Classes:
  PlaceDTO       — outbound: model → JSON (camelCase), validated with Pydantic
  CreatePlaceDTO — inbound:  JSON → new model, validated with Pydantic
  UpdatePlaceDTO — inbound:  JSON → update existing model, validated with Pydantic
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .asset_dto import AssetDTO


class PlaceDTO(BaseModel):
    """Outbound representation of a Place (model → JSON)."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id:          int
    name:        str
    description: Optional[str]    = None
    main_asset:  Optional[AssetDTO] = None

    @classmethod
    def from_model(cls, place) -> dict:
        """Serialize a Place ORM instance to a camelCase dict ready for jsonify."""
        return cls.model_validate(place).model_dump(by_alias=True)


class CreatePlaceDTO(BaseModel):
    """Inbound payload for creating a new place (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          str           = Field(min_length=1)
    description:   Optional[str] = None
    main_asset_id: Optional[int] = None

    @classmethod
    def from_request(cls, data: dict) -> 'CreatePlaceDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)


class UpdatePlaceDTO(BaseModel):
    """Inbound payload for updating an existing place (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          Optional[str] = Field(default=None, min_length=1)
    description:   Optional[str] = None
    main_asset_id: Optional[int] = None

    @classmethod
    def from_request(cls, data: dict) -> 'UpdatePlaceDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)
