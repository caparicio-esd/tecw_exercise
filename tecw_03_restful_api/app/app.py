"""
app.py — Application factory and entry point.

Creates and configures the Flask app, registers blueprints,
sets up the database, migration engine, CLI commands and error handlers.
"""
import logging

import click
from flask import Flask, jsonify
from flask.cli import with_appcontext
from flask_migrate import Migrate
from pydantic import ValidationError

from .blueprints.activity_records import activity_records_bp
from .blueprints.assets import assets_bp
from .blueprints.blocks import blocks_bp
from .blueprints.places import places_bp
from .blueprints.users import users_bp
from .blueprints.ways import ways_bp
from .db import db
from .models import User, Way, Block, Place, Asset, ActivityRecord  # noqa: F401 — registers models with SQLAlchemy

logging.basicConfig(level=logging.DEBUG)

app = Flask(
    __name__
)

app.secret_key = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tecw_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------

app.register_blueprint(blocks_bp, url_prefix="/api/v1/blocks")
app.register_blueprint(users_bp, url_prefix="/api/v1/users")
app.register_blueprint(ways_bp, url_prefix="/api/v1/ways")
app.register_blueprint(places_bp, url_prefix="/api/v1/places")
app.register_blueprint(assets_bp, url_prefix="/api/v1/assets")
app.register_blueprint(activity_records_bp, url_prefix="/api/v1/activity-records")


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    """Return 422 with Pydantic validation details when a DTO fails validation."""
    return jsonify({"error": "Validation failed", "details": e.errors()}), 422


@app.errorhandler(Exception)
def handle_error(e):
    """Catch-all error handler — returns the HTTP status code and error description as JSON."""
    code = e.code if hasattr(e, 'code') else 500
    return jsonify({"error": str(e)}), code

# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

@click.command(name='seed')
@with_appcontext
def seed():
    """Populate the database with initial fixture data."""
    from .seeders import seed_all
    seed_all()


@click.command(name='reset-db')
@with_appcontext
def reset_db():
    """Drop all tables and recreate them (destructive — dev only)."""
    db.drop_all()
    db.create_all()


app.cli.add_command(seed)
app.cli.add_command(reset_db)

# ---------------------------------------------------------------------------
# Let's go
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(
        debug=True
    )
