"""
blueprints/activity_records.py — ActivityRecord REST endpoints.

Base URL: /api/v1/activity-records

An activity record represents a climbing session logged by a user,
linked to either a way or a block, with optional notes and media assets.

Routes:
  GET    /            → list all activity records
  GET    /<id>        → get a single activity record by id
  POST   /            → create a new activity record
  DELETE /<id>        → delete an activity record
"""

from flask import Blueprint, jsonify, request

from ..db import db
from ..models.activity_records import ActivityRecord

activity_records_bp = Blueprint('activity_records', __name__)


@activity_records_bp.route('')
def get_all():
    """Return a list of all activity records."""
    records = ActivityRecord.query.all()
    return jsonify([_serialize(r) for r in records])


@activity_records_bp.route('/<int:activity_record_id>')
def get_by_id(activity_record_id):
    """Return a single activity record identified by *activity_record_id*."""
    record = ActivityRecord.query.get_or_404(activity_record_id)
    return jsonify(_serialize(record))


@activity_records_bp.route('', methods=['POST'])
def create():
    """Create and persist a new activity record from the request body."""
    data = request.get_json()
    record = ActivityRecord(
        user_id=data['user_id'],
        way_id=data.get('way_id'),
        block_id=data.get('block_id'),
        date=data['date'],
        notes=data.get('notes'),
        main_asset_id=data.get('main_asset_id'),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(_serialize(record)), 201


@activity_records_bp.route('/<int:activity_record_id>', methods=['DELETE'])
def delete(activity_record_id):
    """Delete the activity record identified by *activity_record_id*."""
    record = ActivityRecord.query.get_or_404(activity_record_id)
    db.session.delete(record)
    db.session.commit()
    return '', 204


def _serialize(record):
    return {
        'id':            record.id,
        'user_id':       record.user_id,
        'way_id':        record.way_id,
        'block_id':      record.block_id,
        'date':          record.date,
        'notes':         record.notes,
        'main_asset_id': record.main_asset_id,
    }
