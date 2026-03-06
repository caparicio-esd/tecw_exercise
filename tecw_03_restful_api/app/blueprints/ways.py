"""
blueprints/ways.py — Way REST endpoints.

Base URL: /api/v1/ways

Routes:
  GET    /            → list all ways
  GET    /<id>        → get a single way by id
  POST   /            → create a new way
  PUT    /<id>        → replace an existing way
  DELETE /<id>        → delete a way
"""

from typing import Optional

from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from ..auth.decorators import require_auth
from ..db import db
from ..models.ways import Way
from ..dtos.way_dto import WayDTO, CreateWayDTO, UpdateWayDTO
from .query_utils import apply_list_params
from .response_models import WayListResponse

_TAG = Tag(name='Ways')
_SECURITY = [{"BearerAuth": []}]

ways_bp = APIBlueprint('ways', __name__, abp_tags=[_TAG])


class WayPath(BaseModel):
    way_id: int


class WayQuery(BaseModel):
    page:     Optional[int] = 1
    per_page: Optional[int] = 20
    sort:     Optional[str] = 'id'
    order:    Optional[str] = 'asc'
    name:     Optional[str] = None
    grade:    Optional[str] = None
    type:     Optional[str] = None
    city:     Optional[str] = None
    active:   Optional[str] = None


@ways_bp.get('', responses={200: WayListResponse})
def get_all(query: WayQuery):
    """Return a paginated, filterable, sortable list of ways."""
    items, meta = apply_list_params(
        Way,
        Way.query,
        filterable={
            'name':   'like',
            'grade':  'exact',
            'type':   'exact',
            'city':   'exact',
            'active': 'exact',
        },
        sortable=['id', 'name', 'grade', 'length', 'city'],
    )
    return jsonify({'data': [WayDTO.from_model(w) for w in items], 'pagination': meta})


@ways_bp.get('/<int:way_id>', responses={200: WayDTO})
def get_by_id(path: WayPath):
    """Return a single way identified by way_id."""
    return jsonify(WayDTO.from_model(Way.query.get_or_404(path.way_id)))


@ways_bp.post('', security=_SECURITY, responses={201: WayDTO})
@require_auth
def create(body: CreateWayDTO):
    """Create and persist a new way from the request body."""
    way = Way(
        name=body.name,
        grade=body.grade,
        type=body.type,
        length=body.length,
        city=body.city,
        active=body.active,
        description=body.description,
        main_asset_id=body.main_asset_id,
    )
    db.session.add(way)
    db.session.commit()
    return jsonify(WayDTO.from_model(way)), 201


@ways_bp.put('/<int:way_id>', security=_SECURITY, responses={200: WayDTO})
@require_auth
def update(path: WayPath, body: UpdateWayDTO):
    """Replace fields of an existing way identified by way_id."""
    way = Way.query.get_or_404(path.way_id)
    way.name          = body.name          or way.name
    way.grade         = body.grade         or way.grade
    way.type          = body.type          or way.type
    way.length        = body.length        if body.length        is not None else way.length
    way.city          = body.city          or way.city
    way.active        = body.active        if body.active        is not None else way.active
    way.description   = body.description   or way.description
    way.main_asset_id = body.main_asset_id if body.main_asset_id is not None else way.main_asset_id
    db.session.commit()
    return jsonify(WayDTO.from_model(way))


@ways_bp.delete('/<int:way_id>', security=_SECURITY, responses={204: None})
@require_auth
def delete(path: WayPath):
    """Delete the way identified by way_id."""
    way = Way.query.get_or_404(path.way_id)
    db.session.delete(way)
    db.session.commit()
    return '', 204
