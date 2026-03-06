"""
dtos/block_dto.py — Data Transfer Objects for Block.

Classes:
  BlockSummaryDTO — minimal block info for embedding inside activity records
  BlockDTO        — outbound: model → JSON (camelCase), with resolved relations
  CreateBlockDTO  — inbound:  JSON → new model, validated with Pydantic
  UpdateBlockDTO  — inbound:  JSON → update existing model, validated with Pydantic
"""

import re
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from .asset_dto import AssetDTO

_VALID_GRADES = (
    'VB', 'V0', 'V1', 'V2', 'V3', 'V4',
    'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
    'V11', 'V12', 'V13', 'V14', 'V15', 'V16',
)
_HEX_COLOR_RE = re.compile(r'^#[0-9a-fA-F]{6}$')

_CONFIG = ConfigDict(
    from_attributes=True,
    alias_generator=to_camel,
    populate_by_name=True,
)


class BlockSummaryDTO(BaseModel):
    """Minimal block representation for embedding inside activity records (avoids circular nesting)."""

    model_config = _CONFIG

    id:         int
    name:       str
    grade:      str
    color:      str
    city:       str
    main_asset: Optional[AssetDTO] = None


class BlockDTO(BaseModel):
    """Full outbound representation of a Block (model → JSON)."""

    model_config = _CONFIG

    id:          int
    name:        str
    grade:       str
    color:       str
    sector:      str
    height:      float
    city:        str
    active:      bool
    description: Optional[str]    = None
    main_asset:  Optional[AssetDTO] = None
    # Forward reference — resolved by activity_record_dto.model_rebuild() at import time
    activity_records: List['ActivityRecordForBlockDTO'] = []

    @classmethod
    def from_model(cls, block) -> dict:
        """Serialize a Block ORM instance to a camelCase dict ready for jsonify."""
        return cls.model_validate(block).model_dump(by_alias=True)


class CreateBlockDTO(BaseModel):
    """Inbound payload for creating a new block (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          str            = Field(min_length=1)
    grade:         str
    color:         str
    sector:        str            = Field(min_length=1)
    height:        float          = Field(gt=0)
    city:          str            = Field(min_length=1)
    active:        bool           = True
    description:   Optional[str]  = None
    main_asset_id: Optional[int]  = None

    @field_validator('grade')
    @classmethod
    def grade_must_be_valid(cls, v: str) -> str:
        if v not in _VALID_GRADES:
            raise ValueError(f"grade must be one of: {', '.join(_VALID_GRADES)}")
        return v

    @field_validator('color')
    @classmethod
    def color_must_be_hex(cls, v: str) -> str:
        if not _HEX_COLOR_RE.match(v):
            raise ValueError('color must be a valid hex code (e.g. #e74c3c)')
        return v

    @classmethod
    def from_request(cls, data: dict) -> 'CreateBlockDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)


class UpdateBlockDTO(BaseModel):
    """Inbound payload for updating an existing block (JSON → model)."""

    model_config = ConfigDict(populate_by_name=True)

    name:          Optional[str]   = Field(default=None, min_length=1)
    grade:         Optional[str]   = None
    color:         Optional[str]   = None
    sector:        Optional[str]   = Field(default=None, min_length=1)
    height:        Optional[float] = Field(default=None, gt=0)
    city:          Optional[str]   = Field(default=None, min_length=1)
    active:        Optional[bool]  = None
    description:   Optional[str]   = None
    main_asset_id: Optional[int]   = None

    @field_validator('grade')
    @classmethod
    def grade_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in _VALID_GRADES:
            raise ValueError(f"grade must be one of: {', '.join(_VALID_GRADES)}")
        return v

    @field_validator('color')
    @classmethod
    def color_must_be_hex(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not _HEX_COLOR_RE.match(v):
            raise ValueError('color must be a valid hex code (e.g. #e74c3c)')
        return v

    @classmethod
    def from_request(cls, data: dict) -> 'UpdateBlockDTO':
        """Parse and validate a request body dict. Raises ValidationError on invalid input."""
        return cls.model_validate(data)
