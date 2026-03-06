"""
dtos/utils.py — Shared DTO utilities.
"""


def to_camel(snake: str) -> str:
    """Convert a snake_case string to camelCase."""
    parts = snake.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])


def camelize(d: dict) -> dict:
    """Return a new dict with all keys converted from snake_case to camelCase."""
    return {to_camel(k): v for k, v in d.items()}
