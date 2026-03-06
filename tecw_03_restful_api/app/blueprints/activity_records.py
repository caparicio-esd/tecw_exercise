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

from typing import Optional

from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from ..auth.decorators import require_auth
from ..db import db
from ..models.activity_records import ActivityRecord
from ..dtos.activity_record_dto import ActivityRecordDTO, CreateActivityRecordDTO
from .query_utils import apply_list_params
from .response_models import ActivityRecordListResponse

_TAG = Tag(name='ActivityRecords')
_SECURITY = [{"BearerAuth": []}]

activity_records_bp = APIBlueprint('activity_records', __name__, abp_tags=[_TAG])


class ActivityRecordPath(BaseModel):
    activity_record_id: int


class ActivityRecordQuery(BaseModel):
    page:     Optional[int] = 1
    per_page: Optional[int] = 20
    sort:     Optional[str] = 'id'
    order:    Optional[str] = 'asc'
    user_id:  Optional[int] = None
    way_id:   Optional[int] = None
    block_id: Optional[int] = None
    date:     Optional[str] = None


@activity_records_bp.get('', responses={200: ActivityRecordListResponse})
def get_all(query: ActivityRecordQuery):
    """Return a paginated, filterable, sortable list of activity records."""
    items, meta = apply_list_params(
        ActivityRecord,
        ActivityRecord.query,
        filterable={
            'user_id':  'exact',
            'way_id':   'exact',
            'block_id': 'exact',
            'date':     'exact',
        },
        sortable=['id', 'date', 'user_id'],
    )
    return jsonify({'data': [ActivityRecordDTO.from_model(r) for r in items], 'pagination': meta})


@activity_records_bp.get('/<int:activity_record_id>', responses={200: ActivityRecordDTO})
def get_by_id(path: ActivityRecordPath):
    """Return a single activity record identified by activity_record_id."""
    return jsonify(ActivityRecordDTO.from_model(ActivityRecord.query.get_or_404(path.activity_record_id)))


@activity_records_bp.post('', security=_SECURITY, responses={201: ActivityRecordDTO})
@require_auth
def create(body: CreateActivityRecordDTO):
    """Create and persist a new activity record from the request body."""
    record = ActivityRecord(
        user_id=body.user_id,
        way_id=body.way_id,
        block_id=body.block_id,
        date=db.func.current_date(),
        notes=body.notes,
        main_asset_id=body.main_asset_id,
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(ActivityRecordDTO.from_model(record)), 201


@activity_records_bp.delete('/<int:activity_record_id>', security=_SECURITY, responses={204: None})
@require_auth
def delete(path: ActivityRecordPath):
    """Delete the activity record identified by activity_record_id."""
    record = ActivityRecord.query.get_or_404(path.activity_record_id)
    db.session.delete(record)
    db.session.commit()
    return '', 204
