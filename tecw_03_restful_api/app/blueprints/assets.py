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

from typing import Optional

from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from ..auth.decorators import require_auth
from ..db import db
from ..models.assets import Asset
from ..dtos.asset_dto import AssetDTO, CreateAssetDTO
from .query_utils import apply_list_params
from .response_models import AssetListResponse

_TAG = Tag(name='Assets')
_SECURITY = [{"BearerAuth": []}]

assets_bp = APIBlueprint('assets', __name__, abp_tags=[_TAG])


class AssetPath(BaseModel):
    asset_id: int


class AssetQuery(BaseModel):
    page:     Optional[int] = 1
    per_page: Optional[int] = 20
    sort:     Optional[str] = 'id'
    order:    Optional[str] = 'asc'
    url:      Optional[str] = None


@assets_bp.get('', responses={200: AssetListResponse})
def get_all(query: AssetQuery):
    """Return a paginated, filterable, sortable list of assets."""
    items, meta = apply_list_params(
        Asset,
        Asset.query,
        filterable={'url': 'like'},
        sortable=['id', 'url'],
    )
    return jsonify({'data': [AssetDTO.from_model(a) for a in items], 'pagination': meta})


@assets_bp.get('/<int:asset_id>', responses={200: AssetDTO})
def get_by_id(path: AssetPath):
    """Return a single asset identified by asset_id."""
    return jsonify(AssetDTO.from_model(Asset.query.get_or_404(path.asset_id)))


@assets_bp.post('', security=_SECURITY, responses={201: AssetDTO})
@require_auth
def create(body: CreateAssetDTO):
    """Register a new asset from the request body."""
    asset = Asset(url=body.url)
    db.session.add(asset)
    db.session.commit()
    return jsonify(AssetDTO.from_model(asset)), 201


@assets_bp.delete('/<int:asset_id>', security=_SECURITY, responses={204: None})
@require_auth
def delete(path: AssetPath):
    """Delete the asset identified by asset_id."""
    asset = Asset.query.get_or_404(path.asset_id)
    db.session.delete(asset)
    db.session.commit()
    return '', 204
