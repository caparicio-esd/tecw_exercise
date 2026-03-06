"""
fixtures/users.py — User fixture data.

Level is stored as an integer:
  0 = Principiante, 1 = Intermedio, 2 = Avanzado, 3 = Experto

main_asset_id references an asset from the assets fixture.
assets list contains additional asset ids linked via the n--n table.
"""

USERS = [
    {
        "name": "Ana García",
        "email": "admin@tecw.es",
        "avatar": "🧗",
        "level": 2,
        "member_since": "2024-01-15",
        "sessions": 47,
        "active": True,
        "role": "admin",
        "password": "password",
        "main_asset_id": 13,
        "assets": [13],
    },
    {
        "name": "Carlos Pérez",
        "email": "carlos@tecw.es",
        "avatar": "🏔️",
        "level": 1,
        "member_since": "2024-06-03",
        "sessions": 22,
        "active": True,
        "role": "user",
        "password": "password",
        "main_asset_id": 14,
        "assets": [14],
    },
    {
        "name": "Laura Martín",
        "email": "laura@tecw.es",
        "avatar": "🌟",
        "level": 0,
        "member_since": "2025-02-10",
        "sessions": 8,
        "active": True,
        "role": "user",
        "password": "password",
        "main_asset_id": 15,
        "assets": [15],
    },
    {
        "name": "David López",
        "email": "david@tecw.es",
        "avatar": "⛰️",
        "level": 3,
        "member_since": "2023-09-20",
        "sessions": 112,
        "active": False,
        "role": "user",
        "password": "password",
        "main_asset_id": 16,
        "assets": [16],
    },
]
