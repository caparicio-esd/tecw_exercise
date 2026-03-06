"""
dtos/block_dto.py — Data Transfer Objects for Block.

Classes:
  BlockDTO       — outbound: model → JSON (camelCase)
  CreateBlockDTO — inbound:  JSON → new model
  UpdateBlockDTO — inbound:  JSON → update existing model
"""

from dataclasses import dataclass
from typing import Optional

from .utils import camelize


@dataclass
class BlockDTO:
    """Outbound representation of a Block (model → JSON)."""

    id:            int
    name:          str
    grade:         str
    color:         str
    sector:        str
    height:        float
    city:          str
    active:        bool
    description:   Optional[str]
    main_asset_id: Optional[int]

    @staticmethod
    def from_model(block) -> dict:
        """Serialize a Block ORM instance to a camelCase dict ready for jsonify."""
        return camelize({
            'id':            block.id,
            'name':          block.name,
            'grade':         block.grade,
            'color':         block.color,
            'sector':        block.sector,
            'height':        block.height,
            'city':          block.city,
            'active':        block.active,
            'description':   block.description,
            'main_asset_id': block.main_asset_id,
        })


@dataclass
class CreateBlockDTO:
    """Inbound payload for creating a new block (JSON → model)."""

    name:          str
    grade:         str
    color:         str
    sector:        str
    height:        float
    city:          str
    active:        bool          = True
    description:   Optional[str] = None
    main_asset_id: Optional[int] = None

    @staticmethod
    def from_request(data: dict) -> 'CreateBlockDTO':
        """Parse a request body dict into a CreateBlockDTO. Raises KeyError if a required field is missing."""
        return CreateBlockDTO(
            name=data['name'],
            grade=data['grade'],
            color=data['color'],
            sector=data['sector'],
            height=data['height'],
            city=data['city'],
            active=data.get('active', True),
            description=data.get('description'),
            main_asset_id=data.get('main_asset_id'),
        )


@dataclass
class UpdateBlockDTO:
    """Inbound payload for updating an existing block (JSON → model)."""

    name:          Optional[str]   = None
    grade:         Optional[str]   = None
    color:         Optional[str]   = None
    sector:        Optional[str]   = None
    height:        Optional[float] = None
    city:          Optional[str]   = None
    active:        Optional[bool]  = None
    description:   Optional[str]   = None
    main_asset_id: Optional[int]   = None

    @staticmethod
    def from_request(data: dict) -> 'UpdateBlockDTO':
        """Parse a request body dict into an UpdateBlockDTO."""
        return UpdateBlockDTO(
            name=data.get('name'),
            grade=data.get('grade'),
            color=data.get('color'),
            sector=data.get('sector'),
            height=data.get('height'),
            city=data.get('city'),
            active=data.get('active'),
            description=data.get('description'),
            main_asset_id=data.get('main_asset_id'),
        )
