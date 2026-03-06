"""
models/ways.py — Way ORM model.

Represents a climbing route (vía) available at the gym.
Grade follows the French sport climbing scale; type is one of the
three disciplines offered at the facility.

Relationships:
  - assets (n--n via way_assets): all media files attached to this way.
  - main_asset_id: optional FK pointing to the cover image asset.
"""

from ..db import db
from .associations import way_assets

way_grade = db.Enum(
    '3', '4a', '4b', '4c',
    '5a', '5b', '5c',
    '6a', '6a+', '6b', '6b+', '6c', '6c+',
    '7a', '7a+', '7b', '7b+', '7c', '7c+',
    '8a', '8a+', '8b', '8b+', '8c', '8c+',
    name='way_grades'
)
way_type = db.Enum('deportiva', 'top-rope', 'boulder', name='way_types')


class Way(db.Model):
    __tablename__ = "ways"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    grade         = db.Column(way_grade, nullable=False)          # French sport climbing scale
    type          = db.Column(way_type,  nullable=False)          # Deportiva / Top-rope / Boulder
    length        = db.Column(db.Integer, nullable=False)         # metres
    city          = db.Column(db.String(50), nullable=False)      # madrid / barcelona
    active        = db.Column(db.Boolean, default=True)
    description   = db.Column(db.Text, nullable=True)
    main_asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)

    assets = db.relationship('Asset', secondary=way_assets, backref='ways', lazy='dynamic')

    def __repr__(self):
        return f"<Way {self.name} ({self.grade})>"
