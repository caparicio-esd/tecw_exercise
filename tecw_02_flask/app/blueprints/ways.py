"""
blueprints/ways.py — CRUD routes for climbing ways (vías).

All routes require an authenticated session and appropriate role permissions.
The `load_way` decorator resolves the `way_id` URL parameter into a Way
instance before the view function is called.

After every response, an `X-Total-Ways` header is added with the current
total count of ways in the database.
"""

from functools import wraps

from flask import Blueprint, render_template, redirect, request, abort

from ..access_control import check_session, check_role
from ..db import db
from ..handle_files import save_file
from ..models import Way

way_bp = Blueprint('ways', __name__, template_folder="templates", static_folder="static")


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

@way_bp.after_request
def add_total_ways_header(response):
    """Append the total number of ways to every response as a custom header."""
    response.headers['X-Total-Ways'] = Way.query.count()
    return response


def load_way(f):
    """
    Decorator that resolves `way_id` from URL kwargs into a Way ORM object.

    Pops `way_id` from kwargs, queries the database, and injects the resulting
    `way` instance. Aborts with 404 if the way does not exist.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        way_id = kwargs.pop('way_id', None)
        if way_id is not None:
            way = Way.query.get(way_id)
            if way is None:
                abort(404)
            kwargs['way'] = way
        return f(*args, **kwargs)
    return decorated_function


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@way_bp.route('/', methods=['GET'])
@check_session
@check_role
def get_ways():
    """List all climbing ways."""
    ways = Way.query.all()
    return render_template('ways/ways_list.html', ways=ways)


@way_bp.route('/new', methods=['GET'])
@check_session
@check_role
def new_way():
    """Render the form to create a new way."""
    return render_template('ways/way_new.html')


@way_bp.route('/', methods=['POST'])
@check_session
@check_role
@save_file
def create_way(picture=None):
    """
    Persist a new Way from the submitted form data.

    The optional `picture` argument is injected by the `save_file` decorator.
    """
    way = Way(
        name=request.form['name'],
        grade=request.form['grade'],
        type=request.form['type'],
        length=int(request.form['length']),
        city=request.form['city'],
        active=True,
        picture=picture,
        description=request.form['description'],
    )
    db.session.add(way)
    db.session.commit()
    return redirect("/ways")


@way_bp.route('/<int:way_id>')
@check_session
@check_role
@load_way
def get_way_by_id(way):
    """Render the detail page for a single way."""
    return render_template('ways/way_detail.html', way=way)


@way_bp.route('/<int:way_id>/edit', methods=['GET'])
@check_session
@check_role
@load_way
def edit_way(way):
    """Render the edit form for an existing way."""
    return render_template('ways/way_edit.html', way=way)


@way_bp.route('/<int:way_id>/edit', methods=['POST'])
@check_session
@check_role
@load_way
@save_file
def update_way(way, picture=None):
    """
    Update an existing Way with the submitted form data.

    Only replaces the picture if a new file was uploaded.
    """
    way.name        = request.form['name']
    way.grade       = request.form['grade']
    way.type        = request.form['type']
    way.length      = int(request.form['length'])
    way.city        = request.form['city']
    way.description = request.form['description']
    if picture:
        way.picture = picture
    db.session.commit()
    return redirect(f"/ways/{way.id}")


@way_bp.route('/<int:way_id>/delete', methods=['POST'])
@check_session
@check_role
@load_way
def delete_way(way):
    """Delete an existing Way from the database."""
    db.session.delete(way)
    db.session.commit()
    return redirect("/ways")
