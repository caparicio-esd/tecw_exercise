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

from flask import Blueprint, jsonify, request

from ..db import db
from ..models.blocks import Block
from ..dtos.block_dto import BlockDTO, CreateBlockDTO, UpdateBlockDTO

blocks_bp = Blueprint('blocks', __name__)


@blocks_bp.route('')
def get_all():
    """Return a list of all bouldering blocks."""
    return jsonify([BlockDTO.from_model(b) for b in Block.query.all()])


@blocks_bp.route('/<int:block_id>')
def get_by_id(block_id):
    """Return a single block identified by *block_id*."""
    return jsonify(BlockDTO.from_model(Block.query.get_or_404(block_id)))


@blocks_bp.route('', methods=['POST'])
def create():
    """Create and persist a new block from the request body."""
    dto = CreateBlockDTO.from_request(request.get_json())
    block = Block(
        name=dto.name,
        grade=dto.grade,
        color=dto.color,
        sector=dto.sector,
        height=dto.height,
        city=dto.city,
        active=dto.active,
        description=dto.description,
        main_asset_id=dto.main_asset_id,
    )
    db.session.add(block)
    db.session.commit()
    return jsonify(BlockDTO.from_model(block)), 201


@blocks_bp.route('/<int:block_id>', methods=['PUT'])
def update(block_id):
    """Replace all fields of an existing block identified by *block_id*."""
    block = Block.query.get_or_404(block_id)
    dto = UpdateBlockDTO.from_request(request.get_json())
    block.name          = dto.name          or block.name
    block.grade         = dto.grade         or block.grade
    block.color         = dto.color         or block.color
    block.sector        = dto.sector        or block.sector
    block.height        = dto.height        if dto.height        is not None else block.height
    block.city          = dto.city          or block.city
    block.active        = dto.active        if dto.active        is not None else block.active
    block.description   = dto.description   or block.description
    block.main_asset_id = dto.main_asset_id if dto.main_asset_id is not None else block.main_asset_id
    db.session.commit()
    return jsonify(BlockDTO.from_model(block))


@blocks_bp.route('/<int:block_id>', methods=['DELETE'])
def delete(block_id):
    """Delete the block identified by *block_id*."""
    block = Block.query.get_or_404(block_id)
    db.session.delete(block)
    db.session.commit()
    return '', 204
