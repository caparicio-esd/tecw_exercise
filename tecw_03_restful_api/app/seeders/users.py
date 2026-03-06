"""
seeders/users.py — User seeder.

Requires assets to be seeded first (main_asset_id FK + n--n assets).
"""

from ..db import db
from ..fixtures.users import USERS
from ..models.users import User
from ..models.assets import Asset


def seed_users():
    """Insert all users from the USERS fixture into the database."""
    for u in USERS:
        user = User(
            name=u['name'],
            email=u['email'],
            avatar=u['avatar'],
            level=u['level'],
            member_since=u['member_since'],
            sessions=u['sessions'],
            active=u['active'],
            role=u['role'],
            main_asset_id=u.get('main_asset_id'),
        )
        user.set_password(u['password'])

        for asset_id in u.get('assets', []):
            asset = Asset.query.get(asset_id)
            if asset:
                user.assets.append(asset)

        db.session.add(user)

    db.session.commit()
    print(f"{len(USERS)} users inserted")
