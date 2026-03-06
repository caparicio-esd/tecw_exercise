"""
dtos/activity_record_dto.py — Data Transfer Objects for ActivityRecord.

This module also resolves the forward references declared in UserDTO, WayDTO and
BlockDTO by calling model_rebuild() once all contextual DTOs are defined.

Classes:
  ActivityRecordForUserDTO  — record embedded in UserDTO  (no user field)
  ActivityRecordForWayDTO   — record embedded in WayDTO   (no way field)
  ActivityRecordForBlockDTO — record embedded in BlockDTO (no block field)
  ActivityRecordDTO         — full record for the /activity-records endpoint
  CreateActivityRecordDTO   — inbound: JSON → new model, validated with Pydantic
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .asset_dto import AssetDTO
from .user_dto import UserDTO, UserSummaryDTO
from .way_dto import WayDTO, WaySummaryDTO
from .block_dto import BlockDTO, BlockSummaryDTO

_CONFIG = ConfigDict(
    from_attributes=True,
    alias_generator=to_camel,
    populate_by_name=True,
)


class ActivityRecordForUserDTO(BaseModel):
    """Activity record as seen from a User context — omits user to avoid circular nesting."""

    model_config = _CONFIG

    id:         int
    date:       str
    notes:      Optional[str]        = None
    way:        Optional[WaySummaryDTO]   = None
    block:      Optional[BlockSummaryDTO] = None
    main_asset: Optional[AssetDTO]   = None


class ActivityRecordForWayDTO(BaseModel):
    """Activity record as seen from a Way context — omits way to avoid circular nesting."""

    model_config = _CONFIG

    id:         int
    date:       str
    notes:      Optional[str]           = None
    user:       Optional[UserSummaryDTO] = None
    main_asset: Optional[AssetDTO]      = None


class ActivityRecordForBlockDTO(BaseModel):
    """Activity record as seen from a Block context — omits block to avoid circular nesting."""

    model_config = _CONFIG

    id:         int
    date:       str
    notes:      Optional[str]           = None
    user:       Optional[UserSummaryDTO] = None
    main_asset: Optional[AssetDTO]      = None


class ActivityRecordDTO(BaseModel):
    """Full outbound representation of an ActivityRecord for the /activity-records endpoint."""

    model_config = _CONFIG

    id:         int
    date:       str
    notes:      Optional[str]           = None
    user:       Optional[UserSummaryDTO]  = None
    way:        Optional[WaySummaryDTO]   = None
    block:      Optional[BlockSummaryDTO] = None
    main_asset: Optional[AssetDTO]       = None

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


# ---------------------------------------------------------------------------
# Resolve forward references declared in UserDTO / WayDTO / BlockDTO.
# These models reference ActivityRecord*DTO types that were not yet defined
# when those modules were first imported, so we rebuild them here now that
# all types are available.
# ---------------------------------------------------------------------------

UserDTO.model_rebuild()
WayDTO.model_rebuild()
BlockDTO.model_rebuild()
