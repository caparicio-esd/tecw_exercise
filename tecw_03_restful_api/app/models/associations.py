"""
models/associations.py — Many-to-many association tables for Asset relationships.

Each table links the `assets` table to one of the main entities, allowing
any entity to have multiple associated media files (photos, videos, etc.).

These tables are used as the `secondary` argument in SQLAlchemy relationships.
"""

from ..db import db

user_assets = db.Table(
    'user_assets',
    db.Column('user_id',  db.Integer, db.ForeignKey('users.id'),  primary_key=True),
    db.Column('asset_id', db.Integer, db.ForeignKey('assets.id'), primary_key=True),
)

place_assets = db.Table(
    'place_assets',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('asset_id', db.Integer, db.ForeignKey('assets.id'), primary_key=True),
)

way_assets = db.Table(
    'way_assets',
    db.Column('way_id',   db.Integer, db.ForeignKey('ways.id'),   primary_key=True),
    db.Column('asset_id', db.Integer, db.ForeignKey('assets.id'), primary_key=True),
)

block_assets = db.Table(
    'block_assets',
    db.Column('block_id', db.Integer, db.ForeignKey('blocks.id'), primary_key=True),
    db.Column('asset_id', db.Integer, db.ForeignKey('assets.id'), primary_key=True),
)

activity_record_assets = db.Table(
    'activity_record_assets',
    db.Column('activity_record_id', db.Integer, db.ForeignKey('activity_records.id'), primary_key=True),
    db.Column('asset_id',           db.Integer, db.ForeignKey('assets.id'),           primary_key=True),
)
