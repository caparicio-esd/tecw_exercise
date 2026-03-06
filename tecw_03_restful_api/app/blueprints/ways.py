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
from ..dtos.way_dto import WayDTO, CreateWayDTO, UpdateWayDTO

ways_bp = Blueprint('ways', __name__)


@ways_bp.route('')
def get_all():
    """Return a list of all climbing ways."""
    return jsonify([WayDTO.from_model(w) for w in Way.query.all()])


@ways_bp.route('/<int:way_id>')
def get_by_id(way_id):
    """Return a single way identified by *way_id*."""
    return jsonify(WayDTO.from_model(Way.query.get_or_404(way_id)))


@ways_bp.route('', methods=['POST'])
def create():
    """Create and persist a new way from the request body."""
    dto = CreateWayDTO.from_request(request.get_json())
    way = Way(
        name=dto.name,
        grade=dto.grade,
        type=dto.type,
        length=dto.length,
        city=dto.city,
        active=dto.active,
        description=dto.description,
        main_asset_id=dto.main_asset_id,
    )
    db.session.add(way)
    db.session.commit()
    return jsonify(WayDTO.from_model(way)), 201


@ways_bp.route('/<int:way_id>', methods=['PUT'])
def update(way_id):
    """Replace all fields of an existing way identified by *way_id*."""
    way = Way.query.get_or_404(way_id)
    dto = UpdateWayDTO.from_request(request.get_json())
    way.name          = dto.name          or way.name
    way.grade         = dto.grade         or way.grade
    way.type          = dto.type          or way.type
    way.length        = dto.length        if dto.length        is not None else way.length
    way.city          = dto.city          or way.city
    way.active        = dto.active        if dto.active        is not None else way.active
    way.description   = dto.description   or way.description
    way.main_asset_id = dto.main_asset_id if dto.main_asset_id is not None else way.main_asset_id
    db.session.commit()
    return jsonify(WayDTO.from_model(way))


@ways_bp.route('/<int:way_id>', methods=['DELETE'])
def delete(way_id):
    """Delete the way identified by *way_id*."""
    way = Way.query.get_or_404(way_id)
    db.session.delete(way)
    db.session.commit()
    return '', 204
