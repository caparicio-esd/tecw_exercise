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

from flask import Blueprint, jsonify, request

from ..db import db
from ..models.ways import Way

ways_bp = Blueprint('ways', __name__)


@ways_bp.route('')
def get_all():
    """Return a list of all climbing ways."""
    ways = Way.query.all()
    return jsonify([_serialize(w) for w in ways])


@ways_bp.route('/<int:way_id>')
def get_by_id(way_id):
    """Return a single way identified by *way_id*."""
    way = Way.query.get_or_404(way_id)
    return jsonify(_serialize(way))


@ways_bp.route('', methods=['POST'])
def create():
    """Create and persist a new way from the request body."""
    data = request.get_json()
    way = Way(
        name=data['name'],
        grade=data['grade'],
        type=data['type'],
        length=data['length'],
        city=data['city'],
        active=data.get('active', True),
        description=data.get('description'),
        main_asset_id=data.get('main_asset_id'),
    )
    db.session.add(way)
    db.session.commit()
    return jsonify(_serialize(way)), 201


@ways_bp.route('/<int:way_id>', methods=['PUT'])
def update(way_id):
    """Replace all fields of an existing way identified by *way_id*."""
    way = Way.query.get_or_404(way_id)
    data = request.get_json()
    way.name          = data['name']
    way.grade         = data['grade']
    way.type          = data['type']
    way.length        = data['length']
    way.city          = data['city']
    way.active        = data.get('active', way.active)
    way.description   = data.get('description', way.description)
    way.main_asset_id = data.get('main_asset_id', way.main_asset_id)
    db.session.commit()
    return jsonify(_serialize(way))


@ways_bp.route('/<int:way_id>', methods=['DELETE'])
def delete(way_id):
    """Delete the way identified by *way_id*."""
    way = Way.query.get_or_404(way_id)
    db.session.delete(way)
    db.session.commit()
    return '', 204


def _serialize(way):
    return {
        'id':            way.id,
        'name':          way.name,
        'grade':         way.grade,
        'type':          way.type,
        'length':        way.length,
        'city':          way.city,
        'active':        way.active,
        'description':   way.description,
        'main_asset_id': way.main_asset_id,
    }
