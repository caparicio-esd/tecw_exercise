"""
seeders/blocks.py — Block seeder.

Requires assets to be seeded first.
"""

from ..db import db
from ..fixtures.blocks import BLOCKS
from ..models.blocks import Block
from ..models.assets import Asset


def seed_blocks():
    """Insert all blocks from the BLOCKS fixture into the database."""
    for b in BLOCKS:
        block = Block(
            name=b['name'],
            grade=b['grade'],
            color=b['color'],
            sector=b['sector'],
            height=b['height'],
            city=b['city'],
            active=b['active'],
            description=b.get('description'),
            main_asset_id=b.get('main_asset_id'),
        )

        for asset_id in b.get('assets', []):
            asset = Asset.query.get(asset_id)
            if asset:
                block.assets.append(asset)

        db.session.add(block)

    db.session.commit()
    print(f"{len(BLOCKS)} blocks inserted")
