"""
dtos/activity_record_dto.py — Data Transfer Objects for ActivityRecord.

Classes:
  ActivityRecordDTO       — outbound: model → JSON (camelCase)
  CreateActivityRecordDTO — inbound:  JSON → new model
"""

from dataclasses import dataclass
from typing import Optional

from .utils import camelize


@dataclass
class ActivityRecordDTO:
    """Outbound representation of an ActivityRecord (model → JSON)."""

    id:            int
    user_id:       int
    way_id:        Optional[int]
    block_id:      Optional[int]
    date:          str
    notes:         Optional[str]
    main_asset_id: Optional[int]

    @staticmethod
    def from_model(record) -> dict:
        """Serialize an ActivityRecord ORM instance to a camelCase dict ready for jsonify."""
        return camelize({
            'id':            record.id,
            'user_id':       record.user_id,
            'way_id':        record.way_id,
            'block_id':      record.block_id,
            'date':          record.date,
            'notes':         record.notes,
            'main_asset_id': record.main_asset_id,
        })


@dataclass
class CreateActivityRecordDTO:
    """Inbound payload for creating a new activity record (JSON → model)."""

    user_id:       int
    date:          str
    way_id:        Optional[int] = None
    block_id:      Optional[int] = None
    notes:         Optional[str] = None
    main_asset_id: Optional[int] = None

    @staticmethod
    def from_request(data: dict) -> 'CreateActivityRecordDTO':
        """Parse a request body dict into a CreateActivityRecordDTO. Raises KeyError if a required field is missing."""
        return CreateActivityRecordDTO(
            user_id=data['user_id'],
            date=data['date'],
            way_id=data.get('way_id'),
            block_id=data.get('block_id'),
            notes=data.get('notes'),
            main_asset_id=data.get('main_asset_id'),
        )
