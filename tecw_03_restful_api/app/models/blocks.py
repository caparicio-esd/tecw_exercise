"""
models/blocks.py — Block ORM model.

Represents a bouldering problem (bloque) available at the gym.
Grade follows the Hueco (V-scale) system.

Relationships:
  - assets (n--n via block_assets): all media files attached to this block.
  - main_asset_id: optional FK pointing to the cover image asset.
"""

from ..db import db
from .associations import block_assets

block_grade = db.Enum(
    'VB', 'V0', 'V1', 'V2', 'V3', 'V4',
    'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
    'V11', 'V12', 'V13', 'V14', 'V15', 'V16',
    name='block_grades'
)


class Block(db.Model):
    __tablename__ = "blocks"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    grade         = db.Column(block_grade, nullable=False)        # Hueco V-scale
    color         = db.Column(db.String(7),  nullable=False)      # Hex colour code: #e74c3c
    sector        = db.Column(db.String(5),  nullable=False)
    height        = db.Column(db.Float, nullable=False)           # metres
    city          = db.Column(db.String(50), nullable=False)      # madrid / barcelona
    active        = db.Column(db.Boolean, default=True)
    description   = db.Column(db.Text, nullable=True)
    main_asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)

    assets = db.relationship('Asset', secondary=block_assets, backref='blocks', lazy='dynamic')

    def __repr__(self):
        return f"<Block {self.name} ({self.grade})>"
