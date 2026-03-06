"""
blueprints/common.py — General-purpose routes.

Handles the home page, the about page and the per-city landing pages
that aggregate ways and blocks for a given city.
"""

from flask import Blueprint, render_template

from ..data import WAYS, BLOCKS

common_bp = Blueprint('common_bp', __name__, template_folder="templates", static_folder="static")


@common_bp.route('/')
def home():
    """Render the home page."""
    return render_template("home.html")


@common_bp.route('/about')
def about():
    """Render the about / info page."""
    return render_template("about.html")


@common_bp.route('/city/<city>')
def city(city):
    """
    Render the city landing page with its ways and blocks.

    Only 'madrid' and 'barcelona' are valid city slugs.
    Returns 404 for any other value.
    """
    if city not in ["madrid", "barcelona"]:
        return render_template("404.html"), 404

    city_ways   = [w for w in WAYS   if w['city'] == city]
    city_blocks = [b for b in BLOCKS if b['city'] == city]

    return render_template(
        "city.html",
        city=city,
        ways=city_ways,
        blocks=city_blocks,
    )
