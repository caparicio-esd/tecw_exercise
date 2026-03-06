"""
models/activity_records.py — ActivityRecord ORM model.

Tracks a single climbing session logged by a user. A record is linked
to either a Way or a Block (both optional to allow partial records).

Relationships:
  - assets (n--n via activity_record_assets): photos or videos from the session.
  - main_asset_id: optional FK pointing to the highlight asset of the session.
"""

from ..db import db
from .associations import activity_record_assets


class ActivityRecord(db.Model):
    __tablename__ = "activity_records"

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'),  nullable=False)
    way_id        = db.Column(db.Integer, db.ForeignKey('ways.id'),   nullable=True)
    block_id      = db.Column(db.Integer, db.ForeignKey('blocks.id'), nullable=True)
    date          = db.Column(db.String(10), nullable=False)           # YYYY-MM-DD
    main_asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)
    notes         = db.Column(db.Text, nullable=True)

    assets = db.relationship('Asset', secondary=activity_record_assets, backref='activity_records', lazy='dynamic')

    def __repr__(self):
        return f"<ActivityRecord user={self.user_id} date={self.date}>"
