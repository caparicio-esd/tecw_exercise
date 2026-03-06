"""
app.py — Application factory and entry point.

Creates and configures the Flask app, registers blueprints,
sets up the database, migration engine, CLI commands and error handlers.
"""

import logging

import click
from flask import Flask, render_template, request
from flask.cli import with_appcontext
from flask_migrate import Migrate

from .blueprints import block_bp, users_bp, way_bp, common_bp, auth_bp
from .db import db
from .models import User, Way, Block  # noqa: F401 — required so SQLAlchemy registers the models

logging.basicConfig(level=logging.DEBUG)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="public",
    static_url_path=""
)

app.secret_key = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tecw.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------

app.register_blueprint(block_bp,  url_prefix="/blocks")
app.register_blueprint(users_bp,  url_prefix="/users")
app.register_blueprint(way_bp,    url_prefix="/ways")
app.register_blueprint(auth_bp,   url_prefix="/auth")
app.register_blueprint(common_bp, url_prefix="/")

# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    """Render a custom 404 page when a resource is not found."""
    return render_template("404.html"), 404


@app.errorhandler(403)
def unauthorized(e):
    """Render a custom 403 page when access is forbidden."""
    return render_template("403.html"), 403

# ---------------------------------------------------------------------------
# Request hooks
# ---------------------------------------------------------------------------

@app.before_request
def before_request():
    """Log every incoming request method and path for debugging."""
    logging.debug(f"Request: {request.method} {request.path}")

# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

@click.command(name='seed')
@with_appcontext
def seed():
    """Populate the database with initial fixture data."""
    from .models.seeders.users import seed_users
    from .models.seeders.ways import seed_ways
    from .models.seeders.blocks import seed_blocks
    seed_users()
    seed_ways()
    seed_blocks()


@click.command(name='reset-db')
@with_appcontext
def reset_db():
    """Drop all tables and recreate them (destructive — dev only)."""
    db.drop_all()
    db.create_all()


app.cli.add_command(seed)
app.cli.add_command(reset_db)

if __name__ == '__main__':
    app.run(
        #ssl_context=("certs/cert.pem", "certs/key.pem"),
        debug=True
    )
