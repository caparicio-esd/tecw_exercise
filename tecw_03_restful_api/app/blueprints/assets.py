"""
blueprints/assets.py — Asset REST endpoints.

Base URL: /api/v1/assets

Assets are media files (images, videos) that can be attached to any
entity (users, ways, blocks, places, activity records) via n--n tables.

Routes:
  GET    /            → list all assets
  GET    /<id>        → get a single asset by id
  POST   /            → upload and register a new asset
  DELETE /<id>        → delete an asset record
"""

from flask import Blueprint, jsonify, request

from ..db import db
from ..models.assets import Asset

assets_bp = Blueprint('assets', __name__)


@assets_bp.route('')
def get_all():
    """Return a list of all assets."""
    assets = Asset.query.all()
    return jsonify([_serialize(a) for a in assets])


@assets_bp.route('/<int:asset_id>')
def get_by_id(asset_id):
    """Return a single asset identified by *asset_id*."""
    asset = Asset.query.get_or_404(asset_id)
    return jsonify(_serialize(asset))


@assets_bp.route('', methods=['POST'])
def create():
    """Register a new asset from the request body."""
    data = request.get_json()
    asset = Asset(url=data['url'])
    db.session.add(asset)
    db.session.commit()
    return jsonify(_serialize(asset)), 201


@assets_bp.route('/<int:asset_id>', methods=['DELETE'])
def delete(asset_id):
    """Delete the asset identified by *asset_id*."""
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return '', 204


def _serialize(asset):
    return {
        'id':  asset.id,
        'url': asset.url,
    }
