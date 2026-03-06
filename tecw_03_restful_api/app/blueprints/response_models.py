"""
blueprints/response_models.py — Pydantic models used only for OpenAPI response documentation.

These wrapper models describe the JSON envelopes that list endpoints return:
  { "data": [...], "pagination": { ... } }
"""

from typing import List

from pydantic import BaseModel

from ..dtos.way_dto import WayDTO
from ..dtos.block_dto import BlockDTO
from ..dtos.place_dto import PlaceDTO
from ..dtos.asset_dto import AssetDTO
from ..dtos.user_dto import UserDTO
from ..dtos.activity_record_dto import ActivityRecordDTO
from ..dtos.auth_dto import TokenResponseDTO  # noqa: F401 — re-exported for convenience


class PaginationMeta(BaseModel):
    page:       int
    perPage:    int
    total:      int
    totalPages: int


class WayListResponse(BaseModel):
    data:       List[WayDTO]
    pagination: PaginationMeta


class BlockListResponse(BaseModel):
    data:       List[BlockDTO]
    pagination: PaginationMeta


class PlaceListResponse(BaseModel):
    data:       List[PlaceDTO]
    pagination: PaginationMeta


class AssetListResponse(BaseModel):
    data:       List[AssetDTO]
    pagination: PaginationMeta


class UserListResponse(BaseModel):
    data:       List[UserDTO]
    pagination: PaginationMeta


class ActivityRecordListResponse(BaseModel):
    data:       List[ActivityRecordDTO]
    pagination: PaginationMeta
