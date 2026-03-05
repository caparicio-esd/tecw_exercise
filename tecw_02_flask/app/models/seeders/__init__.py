from .users import seed_users
from .ways import seed_ways
from .blocks import seed_blocks


def seed_all():
    seed_users()
    seed_ways()
    seed_blocks()
