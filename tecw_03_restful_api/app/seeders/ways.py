"""
seeders/ways.py — Way seeder.

Requires assets to be seeded first.
"""

from ..db import db
from ..fixtures.ways import WAYS
from ..models.ways import Way
from ..models.assets import Asset


def seed_ways():
    """Insert all ways from the WAYS fixture into the database."""
    for w in WAYS:
        way = Way(
            name=w['name'],
            grade=w['grade'],
            type=w['type'],
            length=w['length'],
            city=w['city'],
            active=w['active'],
            description=w.get('description'),
            main_asset_id=w.get('main_asset_id'),
        )

        for asset_id in w.get('assets', []):
            asset = Asset.query.get(asset_id)
            if asset:
                way.assets.append(asset)

        db.session.add(way)

    db.session.commit()
    print(f"{len(WAYS)} ways inserted")
