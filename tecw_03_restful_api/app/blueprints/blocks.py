"""
blueprints/blocks.py — Block REST endpoints.

Base URL: /api/v1/blocks

Routes:
  GET    /            → list all blocks
  GET    /<id>        → get a single block by id
  POST   /            → create a new block
  PUT    /<id>        → replace an existing block
  DELETE /<id>        → delete a block
"""

from typing import Optional

from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from ..auth.decorators import require_auth
from ..db import db
from ..models.blocks import Block
from ..dtos.block_dto import BlockDTO, CreateBlockDTO, UpdateBlockDTO
from .query_utils import apply_list_params
from .response_models import BlockListResponse

_TAG = Tag(name='Blocks')
_SECURITY = [{"BearerAuth": []}]

blocks_bp = APIBlueprint('blocks', __name__, abp_tags=[_TAG])


class BlockPath(BaseModel):
    block_id: int


class BlockQuery(BaseModel):
    page:     Optional[int] = 1
    per_page: Optional[int] = 20
    sort:     Optional[str] = 'id'
    order:    Optional[str] = 'asc'
    name:     Optional[str] = None
    grade:    Optional[str] = None
    color:    Optional[str] = None
    sector:   Optional[str] = None
    city:     Optional[str] = None
    active:   Optional[str] = None


@blocks_bp.get('', responses={200: BlockListResponse})
def get_all(query: BlockQuery):
    """Return a paginated, filterable, sortable list of blocks."""
    items, meta = apply_list_params(
        Block,
        Block.query,
        filterable={
            'name':   'like',
            'grade':  'exact',
            'color':  'exact',
            'sector': 'exact',
            'city':   'exact',
            'active': 'exact',
        },
        sortable=['id', 'name', 'grade', 'height', 'city'],
    )
    return jsonify({'data': [BlockDTO.from_model(b) for b in items], 'pagination': meta})


@blocks_bp.get('/<int:block_id>', responses={200: BlockDTO})
def get_by_id(path: BlockPath):
    """Return a single block identified by block_id."""
    return jsonify(BlockDTO.from_model(Block.query.get_or_404(path.block_id)))


@blocks_bp.post('', security=_SECURITY, responses={201: BlockDTO})
@require_auth
def create(body: CreateBlockDTO):
    """Create and persist a new block from the request body."""
    block = Block(
        name=body.name,
        grade=body.grade,
        color=body.color,
        sector=body.sector,
        height=body.height,
        city=body.city,
        active=body.active,
        description=body.description,
        main_asset_id=body.main_asset_id,
    )
    db.session.add(block)
    db.session.commit()
    return jsonify(BlockDTO.from_model(block)), 201


@blocks_bp.put('/<int:block_id>', security=_SECURITY, responses={200: BlockDTO})
@require_auth
def update(path: BlockPath, body: UpdateBlockDTO):
    """Replace fields of an existing block identified by block_id."""
    block = Block.query.get_or_404(path.block_id)
    block.name          = body.name          or block.name
    block.grade         = body.grade         or block.grade
    block.color         = body.color         or block.color
    block.sector        = body.sector        or block.sector
    block.height        = body.height        if body.height        is not None else block.height
    block.city          = body.city          or block.city
    block.active        = body.active        if body.active        is not None else block.active
    block.description   = body.description   or block.description
    block.main_asset_id = body.main_asset_id if body.main_asset_id is not None else block.main_asset_id
    db.session.commit()
    return jsonify(BlockDTO.from_model(block))


@blocks_bp.delete('/<int:block_id>', security=_SECURITY, responses={204: None})
@require_auth
def delete(path: BlockPath):
    """Delete the block identified by block_id."""
    block = Block.query.get_or_404(path.block_id)
    db.session.delete(block)
    db.session.commit()
    return '', 204
