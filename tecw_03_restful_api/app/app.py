"""
app.py — Application factory and entry point.

Creates and configures the Flask app, registers blueprints,
sets up the database, migration engine, CLI commands and error handlers.
"""
import logging
import os

import click
from flask import jsonify
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_openapi3 import OpenAPI, Info, SecurityScheme, Tag
from pydantic import ValidationError

from .blueprints.activity_records import activity_records_bp
from .blueprints.assets import assets_bp
from .blueprints.blocks import blocks_bp
from .blueprints.places import places_bp
from .blueprints.users import users_bp
from .blueprints.ways import ways_bp
from .blueprints.auth import auth_bp
from .db import db
from .models import User, Way, Block, Place, Asset, ActivityRecord, RefreshToken  # noqa: F401 — registers models with SQLAlchemy

logging.basicConfig(level=logging.DEBUG)

info = Info(title="TECW API", version="1.0.0")
security_schemes = {"BearerAuth": SecurityScheme(type="http", scheme="bearer")}

app = OpenAPI(
    __name__,
    info=info,
    security_schemes=security_schemes,
    doc_prefix="/docs",
)

app.secret_key = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tecw_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET'] = os.environ.get('JWT_SECRET', 'dev-insecure-secret-change-in-prod')

db.init_app(app)
migrate = Migrate(app, db)

# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------

app.register_api(auth_bp, url_prefix="/api/v1/auth")
app.register_api(blocks_bp, url_prefix="/api/v1/blocks")
app.register_api(users_bp, url_prefix="/api/v1/users")
app.register_api(ways_bp, url_prefix="/api/v1/ways")
app.register_api(places_bp, url_prefix="/api/v1/places")
app.register_api(assets_bp, url_prefix="/api/v1/assets")
app.register_api(activity_records_bp, url_prefix="/api/v1/activity-records")


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
