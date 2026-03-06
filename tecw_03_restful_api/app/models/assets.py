"""
models/assets.py — Asset ORM model.

Represents a media file (image, video, etc.) stored in the system.
Assets are referenced by ways, blocks, places and activity records
through their `main_asset_id` foreign key.
"""

from ..db import db


class Asset(db.Model):
    __tablename__ = "assets"

    id  = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)  # Public URL or relative path to the file

    def __repr__(self):
        return f"<Asset {self.id}: {self.url}>"
