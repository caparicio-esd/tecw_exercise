"""
seeders/__init__.py — Seeder package.

Exposes individual seeders and a convenience seed_all() that runs them
in dependency order: assets must come first since every other entity
references them via FK or n--n tables.
"""

from .assets import seed_assets
from .users import seed_users
from .places import seed_places
from .ways import seed_ways
from .blocks import seed_blocks
from .activity_records import seed_activity_records


def seed_all():
    """Run all seeders in dependency order."""
    seed_assets()
    seed_users()
    seed_places()
    seed_ways()
    seed_blocks()
    seed_activity_records()
