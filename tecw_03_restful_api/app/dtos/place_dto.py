"""
dtos/place_dto.py — Data Transfer Objects for Place.

Classes:
  PlaceDTO       — outbound: model → JSON (camelCase)
  CreatePlaceDTO — inbound:  JSON → new model
  UpdatePlaceDTO — inbound:  JSON → update existing model
"""

from dataclasses import dataclass
from typing import Optional

from .utils import camelize


@dataclass
class PlaceDTO:
    """Outbound representation of a Place (model → JSON)."""

    id:            int
    name:          str
    description:   Optional[str]
    main_asset_id: Optional[int]

    @staticmethod
    def from_model(place) -> dict:
        """Serialize a Place ORM instance to a camelCase dict ready for jsonify."""
        return camelize({
            'id':            place.id,
            'name':          place.name,
            'description':   place.description,
            'main_asset_id': place.main_asset_id,
        })


@dataclass
class CreatePlaceDTO:
    """Inbound payload for creating a new place (JSON → model)."""

    name:          str
    description:   Optional[str] = None
    main_asset_id: Optional[int] = None

    @staticmethod
    def from_request(data: dict) -> 'CreatePlaceDTO':
        """Parse a request body dict into a CreatePlaceDTO. Raises KeyError if a required field is missing."""
        return CreatePlaceDTO(
            name=data['name'],
            description=data.get('description'),
            main_asset_id=data.get('main_asset_id'),
        )


@dataclass
class UpdatePlaceDTO:
    """Inbound payload for updating an existing place (JSON → model)."""

    name:          Optional[str] = None
    description:   Optional[str] = None
    main_asset_id: Optional[int] = None

    @staticmethod
    def from_request(data: dict) -> 'UpdatePlaceDTO':
        """Parse a request body dict into an UpdatePlaceDTO."""
        return UpdatePlaceDTO(
            name=data.get('name'),
            description=data.get('description'),
            main_asset_id=data.get('main_asset_id'),
        )
