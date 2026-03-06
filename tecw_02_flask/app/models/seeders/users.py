"""
models/seeders/users.py — User seeder.

Reads fixture data from data.py and inserts User records into the database.
Every user is assigned the password "password" (hashed at insert time).
"""

from ...data import USERS
from ...db import db
from ..users import User


def seed_users():
    """Insert all users from the USERS fixture into the database."""
    for u in USERS:
        user = User(
            name=u['name'],
            email=u['email'],
            avatar=u['avatar'],
            level=u['level'],
            city=u['city'],
            member_since=u['member_since'],
            sessions=u['sessions'],
            active=u['active'],
            picture=u['picture'],
            role=u.get('role', 'user'),
        )
        user.set_password("password")
        db.session.add(user)
    db.session.commit()
    print(f"{len(USERS)} users inserted")
