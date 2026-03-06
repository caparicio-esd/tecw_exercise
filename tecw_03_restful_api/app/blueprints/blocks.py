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

blocks_bp = Blueprint('blocks', __name__)


@blocks_bp.route('')
def get_all():
    """Return a list of all bouldering blocks."""
    blocks = Block.query.all()
    return jsonify([_serialize(b) for b in blocks])


@blocks_bp.route('/<int:block_id>')
def get_by_id(block_id):
    """Return a single block identified by *block_id*."""
    block = Block.query.get_or_404(block_id)
    return jsonify(_serialize(block))


@blocks_bp.route('', methods=['POST'])
def create():
    """Create and persist a new block from the request body."""
    data = request.get_json()
    block = Block(
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
    db.session.add(block)
    db.session.commit()
    return jsonify(_serialize(block)), 201


@blocks_bp.route('/<int:block_id>', methods=['PUT'])
def update(block_id):
    """Replace all fields of an existing block identified by *block_id*."""
    block = Block.query.get_or_404(block_id)
    data = request.get_json()
    block.name          = data['name']
    block.grade         = data['grade']
    block.color         = data['color']
    block.sector        = data['sector']
    block.height        = data['height']
    block.city          = data['city']
    block.active        = data.get('active', block.active)
    block.description   = data.get('description', block.description)
    block.main_asset_id = data.get('main_asset_id', block.main_asset_id)
    db.session.commit()
    return jsonify(_serialize(block))


@blocks_bp.route('/<int:block_id>', methods=['DELETE'])
def delete(block_id):
    """Delete the block identified by *block_id*."""
    block = Block.query.get_or_404(block_id)
    db.session.delete(block)
    db.session.commit()
    return '', 204


def _serialize(block):
    return {
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
    }
