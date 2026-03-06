"""
app.py — Application factory and entry point.

Creates and configures the Flask app, registers blueprints,
sets up the database, migration engine, CLI commands and error handlers.
"""
import logging
import os
import subprocess

import click
from flask import jsonify, send_from_directory
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


_REACT_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tecw_04_react'))
_REACT_DIST = os.path.join(_REACT_DIR, 'dist')


@click.command(name='build-ui')
@with_appcontext
def build_ui():
    """Build the React frontend and make it available at /."""
    click.echo(f'Building React app at {_REACT_DIR} …')
    result = subprocess.run(['npm', 'run', 'build'], cwd=_REACT_DIR)
    if result.returncode != 0:
        raise click.ClickException('npm build failed')
    click.echo('Done — React app built successfully.')


app.cli.add_command(seed)
app.cli.add_command(reset_db)
app.cli.add_command(build_ui)

# ---------------------------------------------------------------------------
# SPA — serve the React build at /
# Must be registered after all API blueprints so it only catches unknown paths.
# ---------------------------------------------------------------------------

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_spa(path):
    """Serve the React SPA. API and docs routes are matched first by Flask."""
    if not os.path.isdir(_REACT_DIST):
        return jsonify({'error': 'Frontend not built. Run: flask build-ui'}), 503
    # Serve an existing file (JS, CSS, images…) or fall back to index.html (SPA routing).
    target = os.path.join(_REACT_DIST, path)
    if path and os.path.isfile(target):
        return send_from_directory(_REACT_DIST, path)
    return send_from_directory(_REACT_DIST, 'index.html')

# ---------------------------------------------------------------------------
# Let's go
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(
        debug=True
    )
