from ...data import WAYS
from ...db import db
from ..ways import Way


def seed_ways():
    for w in WAYS:
        way = Way(
            name=w['name'],
            grade=w['grade'],
            type=w['type'],
            length=w['length'],
            city=w['city'],
            active=w['active'],
            picture=w['picture'],
            description=w['description'],
        )
        db.session.add(way)
    db.session.commit()
    print(f"{len(WAYS)} vías insertadas")
