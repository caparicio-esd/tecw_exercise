from ...data import USERS
from ...db import db
from ..users import User


def seed_users():
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
        )
        user.set_password("password")
        db.session.add(user)
    db.session.commit()
    print(f"{len(USERS)} usuarios insertados")
