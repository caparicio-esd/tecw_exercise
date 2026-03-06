"""
db.py — SQLAlchemy instance.

Instantiated here without binding to any app so that models can import
`db` without causing circular imports. The app binds it via `db.init_app(app)`
inside app.py.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
