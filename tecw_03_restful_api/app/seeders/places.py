"""
seeders/places.py — Place seeder.

Requires assets to be seeded first.
"""

from ..db import db
from ..fixtures.places import PLACES
from ..models.places import Place
from ..models.assets import Asset


def seed_places():
    """Insert all places from the PLACES fixture into the database."""
    for p in PLACES:
        place = Place(
            name=p['name'],
            description=p.get('description'),
            main_asset_id=p.get('main_asset_id'),
        )

        for asset_id in p.get('assets', []):
            asset = Asset.query.get(asset_id)
            if asset:
                place.assets.append(asset)

        db.session.add(place)

    db.session.commit()
    print(f"{len(PLACES)} places inserted")
