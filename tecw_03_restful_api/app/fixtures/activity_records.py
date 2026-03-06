"""
fixtures/activity_records.py — ActivityRecord fixture data.

user_index, way_index and block_index are 0-based positions in the
USERS, WAYS and BLOCKS fixture lists respectively (resolved at seed time).
Only one of way_index / block_index should be set per record.
assets references asset ids from the assets fixture.
"""

ACTIVITY_RECORDS = [
    {
        "user_index": 0,        # Ana García
        "way_index": 0,         # La Esfinge
        "block_index": None,
        "date": "2025-11-10",
        "notes": "Sent it clean for the first time. Footwork finally clicked.",
        "main_asset_id": 17,
        "assets": [17],
    },
    {
        "user_index": 1,        # Carlos Pérez
        "way_index": None,
        "block_index": 0,       # Bloque Alpha
        "date": "2025-12-03",
        "notes": "Stuck the dyno on the third attempt. Felt strong today.",
        "main_asset_id": 18,
        "assets": [18],
    },
    {
        "user_index": 2,        # Laura Martín
        "way_index": 2,         # Viento del Sur
        "block_index": None,
        "date": "2026-01-15",
        "notes": "First time top-roping this grade. Really enjoyed the movement.",
        "main_asset_id": 19,
        "assets": [19],
    },
    {
        "user_index": 0,        # Ana García
        "way_index": None,
        "block_index": 2,       # Bloque Gamma
        "date": "2026-02-20",
        "notes": "V7 project done! Took three sessions to figure out the beta.",
        "main_asset_id": 20,
        "assets": [20, 17],
    },
]
