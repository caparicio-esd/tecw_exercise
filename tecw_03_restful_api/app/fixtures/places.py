"""
fixtures/places.py — Place fixture data.

Represents the physical zones/sectors of the gym.
main_asset_id and assets reference the assets fixture.
"""

PLACES = [
    {
        "name": "Sala Principal Madrid",
        "description": "Main hall in the Madrid gym. Hosts all lead climbing walls and most boulder problems.",
        "main_asset_id": 10,
        "assets": [10],
    },
    {
        "name": "Boulder Room Madrid",
        "description": "Dedicated bouldering area in Madrid with overhanging walls and a padded floor.",
        "main_asset_id": 11,
        "assets": [11],
    },
    {
        "name": "Sala Principal Barcelona",
        "description": "Main hall in the Barcelona gym. Features the tallest lead walls in the facility.",
        "main_asset_id": 12,
        "assets": [10, 12],
    },
]
