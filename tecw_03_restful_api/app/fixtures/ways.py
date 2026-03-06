"""
fixtures/ways.py — Way fixture data.

grade must be a value from the way_grades Enum defined in models/ways.py.
type  must be one of: 'deportiva', 'top-rope', 'boulder'.
main_asset_id and assets reference the assets fixture.
"""

WAYS = [
    {
        "name": "La Esfinge",
        "grade": "6a",
        "type": "deportiva",
        "length": 12,
        "city": "madrid",
        "active": True,
        "description": "Classic endurance route on slab with rex holds. Great for footwork technique.",
        "main_asset_id": 1,
        "assets": [1, 2],
    },
    {
        "name": "El Cóndor",
        "grade": "7b",
        "type": "deportiva",
        "length": 15,
        "city": "barcelona",
        "active": True,
        "description": "Powerful dynamic move at mid-height with a roof finish. The crux requires a good lunge to a crimp.",
        "main_asset_id": 2,
        "assets": [2],
    },
    {
        "name": "Viento del Sur",
        "grade": "5c",
        "type": "top-rope",
        "length": 10,
        "city": "madrid",
        "active": True,
        "description": "Ideal for beginners. Slab with positive holds and good rest opportunities.",
        "main_asset_id": 3,
        "assets": [3],
    },
    {
        "name": "Pared Norte",
        "grade": "7a+",
        "type": "deportiva",
        "length": 18,
        "city": "barcelona",
        "active": False,
        "description": "Endurance route with finger pockets on an overhang. Currently closed for hold replacement.",
        "main_asset_id": 4,
        "assets": [4],
    },
    {
        "name": "Techo Rojo",
        "grade": "7c",
        "type": "boulder",
        "length": 4,
        "city": "madrid",
        "active": True,
        "description": "Full-roof boulder problem. The elbow sequence is key to topping out.",
        "main_asset_id": 5,
        "assets": [5, 1],
    },
]
