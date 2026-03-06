"""
seeders/assets.py — Asset seeder.

Must run before all other seeders since every other entity
references assets via foreign keys and n--n relationships.
"""

from ..db import db
from ..fixtures.assets import ASSETS
from ..models.assets import Asset


def seed_assets():
    """Insert all assets from the ASSETS fixture into the database."""
    for a in ASSETS:
        asset = Asset(id=a['id'], url=a['url'])
        db.session.add(asset)
    db.session.commit()
    print(f"{len(ASSETS)} assets inserted")
