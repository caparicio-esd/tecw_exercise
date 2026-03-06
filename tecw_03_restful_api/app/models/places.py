"""
models/places.py — Place ORM model.

Represents a physical gym location or sector within the facility.

Relationships:
  - assets (n--n via place_assets): all media files attached to this place.
  - main_asset_id: optional FK pointing to the cover image asset.
"""

from ..db import db
from .associations import place_assets


class Place(db.Model):
    __tablename__ = 'places'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(255), nullable=False)
    description   = db.Column(db.Text, nullable=True)
    main_asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)

    assets = db.relationship('Asset', secondary=place_assets, backref='places', lazy='dynamic')

    def __repr__(self):
        return f'<Place {self.name}>'
