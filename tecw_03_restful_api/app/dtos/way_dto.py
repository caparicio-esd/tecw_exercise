"""
dtos/way_dto.py — Data Transfer Objects for Way.

Classes:
  WayDTO       — outbound: model → JSON (camelCase)
  CreateWayDTO — inbound:  JSON → new model
  UpdateWayDTO — inbound:  JSON → update existing model
"""

from dataclasses import dataclass
from typing import Optional

from .utils import camelize


@dataclass
class WayDTO:
    """Outbound representation of a Way (model → JSON)."""

    id:            int
    name:          str
    grade:         str
    type:          str
    length:        int
    city:          str
    active:        bool
    description:   Optional[str]
    main_asset_id: Optional[int]

    @staticmethod
    def from_model(way) -> dict:
        """Serialize a Way ORM instance to a camelCase dict ready for jsonify."""
        return camelize({
            'id':            way.id,
            'name':          way.name,
            'grade':         way.grade,
            'type':          way.type,
            'length':        way.length,
            'city':          way.city,
            'active':        way.active,
            'description':   way.description,
            'main_asset_id': way.main_asset_id,
        })


@dataclass
class CreateWayDTO:
    """Inbound payload for creating a new way (JSON → model)."""

    name:          str
    grade:         str
    type:          str
    length:        int
    city:          str
    active:        bool          = True
    description:   Optional[str] = None
    main_asset_id: Optional[int] = None

    @staticmethod
    def from_request(data: dict) -> 'CreateWayDTO':
        """Parse a request body dict into a CreateWayDTO. Raises KeyError if a required field is missing."""
        return CreateWayDTO(
            name=data['name'],
            grade=data['grade'],
            type=data['type'],
            length=data['length'],
            city=data['city'],
            active=data.get('active', True),
            description=data.get('description'),
            main_asset_id=data.get('main_asset_id'),
        )


@dataclass
class UpdateWayDTO:
    """Inbound payload for updating an existing way (JSON → model)."""

    name:          Optional[str]  = None
    grade:         Optional[str]  = None
    type:          Optional[str]  = None
    length:        Optional[int]  = None
    city:          Optional[str]  = None
    active:        Optional[bool] = None
    description:   Optional[str]  = None
    main_asset_id: Optional[int]  = None

    @staticmethod
    def from_request(data: dict) -> 'UpdateWayDTO':
        """Parse a request body dict into an UpdateWayDTO."""
        return UpdateWayDTO(
            name=data.get('name'),
            grade=data.get('grade'),
            type=data.get('type'),
            length=data.get('length'),
            city=data.get('city'),
            active=data.get('active'),
            description=data.get('description'),
            main_asset_id=data.get('main_asset_id'),
        )
