"""
fixtures/blocks.py — Block fixture data.

grade must be a value from the block_grades Enum defined in models/blocks.py.
color is a CSS hex code used to visually identify the hold colour.
main_asset_id and assets reference the assets fixture.
"""

BLOCKS = [
    {
        "name": "Bloque Alpha",
        "grade": "V3",
        "color": "#e74c3c",
        "sector": "A",
        "height": 4.0,
        "city": "madrid",
        "active": True,
        "description": "Intro block with technical moves on an overhang. Good for improving grip strength.",
        "main_asset_id": 6,
        "assets": [6],
    },
    {
        "name": "Bloque Beta",
        "grade": "V5",
        "color": "#8e44ad",
        "sector": "B",
        "height": 4.5,
        "city": "madrid",
        "active": True,
        "description": "Dynamic shoulder sequence. Requires coordination and upper-body power.",
        "main_asset_id": 7,
        "assets": [7, 6],
    },
    {
        "name": "Bloque Gamma",
        "grade": "V7",
        "color": "#2c3e50",
        "sector": "A",
        "height": 3.5,
        "city": "barcelona",
        "active": True,
        "description": "Endurance slab problem. Foot placement is the key to unlocking the crux.",
        "main_asset_id": 8,
        "assets": [8],
    },
    {
        "name": "Bloque Delta",
        "grade": "V2",
        "color": "#27ae60",
        "sector": "C",
        "height": 3.0,
        "city": "barcelona",
        "active": False,
        "description": "Beginner block with positive holds. Currently under maintenance.",
        "main_asset_id": 9,
        "assets": [9],
    },
]
