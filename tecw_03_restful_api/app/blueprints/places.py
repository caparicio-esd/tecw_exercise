"""
blueprints/places.py — Place REST endpoints.

Base URL: /api/v1/places

Routes:
  GET    /            → list all places
  GET    /<id>        → get a single place by id
  POST   /            → create a new place
  PUT    /<id>        → replace an existing place
  DELETE /<id>        → delete a place
"""

from typing import Optional

from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from ..auth.decorators import require_auth
from ..db import db
from ..models.places import Place
from ..dtos.place_dto import PlaceDTO, CreatePlaceDTO, UpdatePlaceDTO
from .query_utils import apply_list_params
from .response_models import PlaceListResponse

_TAG = Tag(name='Places')
_SECURITY = [{"BearerAuth": []}]

places_bp = APIBlueprint('places', __name__, abp_tags=[_TAG])


class PlacePath(BaseModel):
    place_id: int


class PlaceQuery(BaseModel):
    page:     Optional[int] = 1
    per_page: Optional[int] = 20
    sort:     Optional[str] = 'id'
    order:    Optional[str] = 'asc'
    name:     Optional[str] = None


@places_bp.get('', responses={200: PlaceListResponse})
def get_all(query: PlaceQuery):
    """Return a paginated, filterable, sortable list of places."""
    items, meta = apply_list_params(
        Place,
        Place.query,
        filterable={'name': 'like'},
        sortable=['id', 'name'],
    )
    return jsonify({'data': [PlaceDTO.from_model(p) for p in items], 'pagination': meta})


@places_bp.get('/<int:place_id>', responses={200: PlaceDTO})
def get_by_id(path: PlacePath):
    """Return a single place identified by place_id."""
    return jsonify(PlaceDTO.from_model(Place.query.get_or_404(path.place_id)))


@places_bp.post('', security=_SECURITY, responses={201: PlaceDTO})
@require_auth
def create(body: CreatePlaceDTO):
    """Create and persist a new place from the request body."""
    place = Place(
        name=body.name,
        description=body.description,
        main_asset_id=body.main_asset_id,
    )
    db.session.add(place)
    db.session.commit()
    return jsonify(PlaceDTO.from_model(place)), 201


@places_bp.put('/<int:place_id>', security=_SECURITY, responses={200: PlaceDTO})
@require_auth
def update(path: PlacePath, body: UpdatePlaceDTO):
    """Replace fields of an existing place identified by place_id."""
    place = Place.query.get_or_404(path.place_id)
    place.name          = body.name          or place.name
    place.description   = body.description   or place.description
    place.main_asset_id = body.main_asset_id if body.main_asset_id is not None else place.main_asset_id
    db.session.commit()
    return jsonify(PlaceDTO.from_model(place))


@places_bp.delete('/<int:place_id>', security=_SECURITY, responses={204: None})
@require_auth
def delete(path: PlacePath):
    """Delete the place identified by place_id."""
    place = Place.query.get_or_404(path.place_id)
    db.session.delete(place)
    db.session.commit()
    return '', 204
