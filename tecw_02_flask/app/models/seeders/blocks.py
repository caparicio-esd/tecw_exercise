from ...data import BLOCKS
from ...db import db
from ..blocks import Block


def seed_blocks():
    for b in BLOCKS:
        block = Block(
            name=b['name'],
            grade=b['grade'],
            color=b['color'],
            sector=b['sector'],
            height=b['height'],
            city=b['city'],
            active=b['active'],
            picture=b['picture'],
            description=b['description'],
        )
        db.session.add(block)
    db.session.commit()
    print(f"{len(BLOCKS)} bloques insertados")
