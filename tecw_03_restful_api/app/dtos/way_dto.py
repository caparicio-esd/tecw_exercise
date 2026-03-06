"""
dtos/way_dto.py — Data Transfer Objects for Way.

Classes:
  WaySummaryDTO  — minimal way info for embedding inside activity records
  WayDTO         — outbound: model → JSON (camelCase), with resolved relations
  CreateWayDTO   — inbound:  JSON → new model, validated with Pydantic
  UpdateWayDTO   — inbound:  JSON → update existing model, validated with Pydantic
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from .asset_dto import AssetDTO

_VALID_GRADES = (
    '3', '4a', '4b', '4c',
    '5a', '5b', '5c',
    '6a', '6a+', '6b', '6b+', '6c', '6c+',
    '7a', '7a+', '7b', '7b+', '7c', '7c+',
    '8a', '8a+', '8b', '8b+', '8c', '8c+',
)
_VALID_TYPES = ('deportiva', 'top-rope', 'boulder')

_CONFIG = ConfigDict(
    from_attributes=True,
    alias_generator=to_camel,
    populate_by_name=True,
)


class WaySummaryDTO(BaseModel):
    """Minimal way representation for embedding inside activity records (avoids circular nesting)."""

    model_config = _CONFIG

    id:         int
    name:       str
    grade:      str
    type:       str
    city:       str
    main_asset: Optional[AssetDTO] = None


class WayDTO(BaseModel):
    """Full outbound representation of a Way (model → JSON)."""

    model_config = _CONFIG

    id:          int
    name:        str
    grade:       str
    type:        str
    length:      int
    city:        str
    active:      bool
    description: Optional[str]    = None
    main_asset:  Optional[AssetDTO] = None
    # Forward reference — resolved by activity_record_dto.model_rebuild() at import time
    activity_records: List['ActivityRecordForWayDTO'] = []

    @classmethod
    def from_model(cls, way) -> dict:
        """Serialize a Way ORM instance to a camelCase dict ready for jsonify."""
        return cls.model_validate(way).model_dump(by_alias=True)


class CreateWayDTO(BaseModel):
    """Inbound payload for creating a new way (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          str           = Field(min_length=1)
    grade:         str
    type:          str
    length:        int           = Field(gt=0)
    city:          str           = Field(min_length=1)
    active:        bool          = True
    description:   Optional[str] = None
    main_asset_id: Optional[int] = None

    @field_validator('grade')
    @classmethod
    def grade_must_be_valid(cls, v: str) -> str:
        if v not in _VALID_GRADES:
            raise ValueError(f"grade must be one of: {', '.join(_VALID_GRADES)}")
        return v

    @field_validator('type')
    @classmethod
    def type_must_be_valid(cls, v: str) -> str:
        if v not in _VALID_TYPES:
            raise ValueError(f"type must be one of: {', '.join(_VALID_TYPES)}")
        return v

    @classmethod
    def from_request(cls, data: dict) -> 'CreateWayDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)


class UpdateWayDTO(BaseModel):
    """Inbound payload for updating an existing way (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          Optional[str]  = Field(default=None, min_length=1)
    grade:         Optional[str]  = None
    type:          Optional[str]  = None
    length:        Optional[int]  = Field(default=None, gt=0)
    city:          Optional[str]  = Field(default=None, min_length=1)
    active:        Optional[bool] = None
    description:   Optional[str]  = None
    main_asset_id: Optional[int]  = None

    @field_validator('grade')
    @classmethod
    def grade_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in _VALID_GRADES:
            raise ValueError(f"grade must be one of: {', '.join(_VALID_GRADES)}")
        return v

    @field_validator('type')
    @classmethod
    def type_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in _VALID_TYPES:
            raise ValueError(f"type must be one of: {', '.join(_VALID_TYPES)}")
        return v

    @classmethod
    def from_request(cls, data: dict) -> 'UpdateWayDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)
