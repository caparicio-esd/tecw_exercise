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

places_bp = Blueprint('places', __name__)


@places_bp.route('')
def get_all():
    """Return a list of all gym places/sectors."""
    places = Place.query.all()
    return jsonify([_serialize(p) for p in places])


@places_bp.route('/<int:place_id>')
def get_by_id(place_id):
    """Return a single place identified by *place_id*."""
    place = Place.query.get_or_404(place_id)
    return jsonify(_serialize(place))


@places_bp.route('', methods=['POST'])
def create():
    """Create and persist a new place from the request body."""
    data = request.get_json()
    place = Place(
        name=data['name'],
        description=data.get('description'),
        main_asset_id=data.get('main_asset_id'),
    )
    db.session.add(place)
    db.session.commit()
    return jsonify(_serialize(place)), 201


@places_bp.route('/<int:place_id>', methods=['PUT'])
def update(place_id):
    """Replace all fields of an existing place identified by *place_id*."""
    place = Place.query.get_or_404(place_id)
    data = request.get_json()
    place.name          = data['name']
    place.description   = data.get('description', place.description)
    place.main_asset_id = data.get('main_asset_id', place.main_asset_id)
    db.session.commit()
    return jsonify(_serialize(place))


@places_bp.route('/<int:place_id>', methods=['DELETE'])
def delete(place_id):
    """Delete the place identified by *place_id*."""
    place = Place.query.get_or_404(place_id)
    db.session.delete(place)
    db.session.commit()
    return '', 204


def _serialize(place):
    return {
        'id':            place.id,
        'name':          place.name,
        'description':   place.description,
        'main_asset_id': place.main_asset_id,
    }
