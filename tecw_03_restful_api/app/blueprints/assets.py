"""
blueprints/assets.py — Asset REST endpoints.

Base URL: /api/v1/assets

Assets are media files (images, videos) that can be attached to any
entity (users, ways, blocks, places, activity records) via n--n tables.

Routes:
  GET    /            → list all assets
  GET    /<id>        → get a single asset by id
  POST   /            → register a new asset
  DELETE /<id>        → delete an asset record
"""

from flask import Blueprint, jsonify, request

from ..db import db
from ..models.assets import Asset
from ..dtos.asset_dto import AssetDTO, CreateAssetDTO

assets_bp = Blueprint('assets', __name__)


@assets_bp.route('')
def get_all():
    """Return a list of all assets."""
    return jsonify([AssetDTO.from_model(a) for a in Asset.query.all()])


@assets_bp.route('/<int:asset_id>')
def get_by_id(asset_id):
    """Return a single asset identified by *asset_id*."""
    return jsonify(AssetDTO.from_model(Asset.query.get_or_404(asset_id)))


@assets_bp.route('', methods=['POST'])
def create():
    """Register a new asset from the request body."""
    dto = CreateAssetDTO.from_request(request.get_json())
    asset = Asset(url=dto.url)
    db.session.add(asset)
    db.session.commit()
    return jsonify(AssetDTO.from_model(asset)), 201


@assets_bp.route('/<int:asset_id>', methods=['DELETE'])
def delete(asset_id):
    """Delete the asset identified by *asset_id*."""
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return '', 204
