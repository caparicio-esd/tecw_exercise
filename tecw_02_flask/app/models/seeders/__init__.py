"""
models/seeders/__init__.py — Seeder package exports.

Exposes individual seeder functions and a convenience `seed_all` function
that runs all seeders in the correct order.
"""

from .users import seed_users
from .ways import seed_ways
from .blocks import seed_blocks


def seed_all():
    """Run all seeders: users, ways, blocks."""
    seed_users()
    seed_ways()
    seed_blocks()
