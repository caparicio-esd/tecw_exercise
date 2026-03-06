"""
dtos/activity_record_dto.py — Data Transfer Objects for ActivityRecord.

Classes:
  ActivityRecordDTO       — outbound: model → JSON (camelCase), validated with Pydantic
  CreateActivityRecordDTO — inbound:  JSON → new model, validated with Pydantic
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ActivityRecordDTO(BaseModel):
    """Outbound representation of an ActivityRecord (model → JSON)."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id:            int
    user_id:       int
    way_id:        Optional[int] = None
    block_id:      Optional[int] = None
    date:          str
    notes:         Optional[str] = None
    main_asset_id: Optional[int] = None

    @classmethod
    def from_model(cls, record) -> dict:
        """Serialize an ActivityRecord ORM instance to a camelCase dict ready for jsonify."""
        return cls.model_validate(record).model_dump(by_alias=True)


class CreateActivityRecordDTO(BaseModel):
    """Inbound payload for creating a new activity record (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    user_id:       int           = Field(gt=0)
    way_id:        Optional[int] = Field(default=None, gt=0)
    block_id:      Optional[int] = Field(default=None, gt=0)
    notes:         Optional[str] = None
    main_asset_id: Optional[int] = None

    @classmethod
    def from_request(cls, data: dict) -> 'CreateActivityRecordDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)
