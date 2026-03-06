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

from flask import Blueprint, jsonify, request

from ..db import db
from ..models.places import Place
from ..dtos.place_dto import PlaceDTO, CreatePlaceDTO, UpdatePlaceDTO
from .query_utils import apply_list_params

places_bp = Blueprint('places', __name__)


@places_bp.route('')
def get_all():
    """Return a paginated, filterable, sortable list of places.

    Filters : name (like)
    Sort by : id (default), name
    """
    items, meta = apply_list_params(
        Place,
        Place.query,
        filterable={'name': 'like'},
        sortable=['id', 'name'],
    )
    return jsonify({'data': [PlaceDTO.from_model(p) for p in items], 'pagination': meta})


@places_bp.route('/<int:place_id>')
def get_by_id(place_id):
    """Return a single place identified by *place_id*."""
    return jsonify(PlaceDTO.from_model(Place.query.get_or_404(place_id)))


@places_bp.route('', methods=['POST'])
def create():
    """Create and persist a new place from the request body."""
    dto = CreatePlaceDTO.from_request(request.get_json())
    place = Place(
        name=dto.name,
        description=dto.description,
        main_asset_id=dto.main_asset_id,
    )
    db.session.add(place)
    db.session.commit()
    return jsonify(PlaceDTO.from_model(place)), 201


@places_bp.route('/<int:place_id>', methods=['PUT'])
def update(place_id):
    """Replace all fields of an existing place identified by *place_id*."""
    place = Place.query.get_or_404(place_id)
    dto = UpdatePlaceDTO.from_request(request.get_json())
    place.name          = dto.name          or place.name
    place.description   = dto.description   or place.description
    place.main_asset_id = dto.main_asset_id if dto.main_asset_id is not None else place.main_asset_id
    db.session.commit()
    return jsonify(PlaceDTO.from_model(place))


@places_bp.route('/<int:place_id>', methods=['DELETE'])
def delete(place_id):
    """Delete the place identified by *place_id*."""
    place = Place.query.get_or_404(place_id)
    db.session.delete(place)
    db.session.commit()
    return '', 204
