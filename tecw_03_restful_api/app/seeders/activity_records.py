"""
seeders/activity_records.py — ActivityRecord seeder.

Requires users, ways, blocks and assets to be seeded first.
user_index / way_index / block_index in the fixture are resolved
to actual DB ids by querying the inserted records in order.
"""

from ..db import db
from ..fixtures.activity_records import ACTIVITY_RECORDS
from ..models.activity_records import ActivityRecord
from ..models.users import User
from ..models.ways import Way
from ..models.blocks import Block
from ..models.assets import Asset


def seed_activity_records():
    """Insert all activity records from the fixture into the database."""
    users  = User.query.order_by(User.id).all()
    ways   = Way.query.order_by(Way.id).all()
    blocks = Block.query.order_by(Block.id).all()

    for r in ACTIVITY_RECORDS:
        user  = users[r['user_index']]
        way   = ways[r['way_index']]     if r.get('way_index')   is not None else None
        block = blocks[r['block_index']] if r.get('block_index') is not None else None

        record = ActivityRecord(
            user_id=user.id,
            way_id=way.id     if way   else None,
            block_id=block.id if block else None,
            date=r['date'],
            notes=r.get('notes'),
            main_asset_id=r.get('main_asset_id'),
        )

        for asset_id in r.get('assets', []):
            asset = Asset.query.get(asset_id)
            if asset:
                record.assets.append(asset)

        db.session.add(record)

    db.session.commit()
    print(f"{len(ACTIVITY_RECORDS)} activity records inserted")
