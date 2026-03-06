"""
blueprints/blocks.py — CRUD routes for bouldering blocks (bloques).

All routes require an authenticated session and appropriate role permissions.
The `load_block` decorator resolves the `block_id` URL parameter into a Block
instance before the view function is called.

After every response, an `X-Total-Blocks` header is added with the current
total count of blocks in the database.
"""

from functools import wraps

from flask import Blueprint, render_template, redirect, request, abort

from ..access_control import check_session, check_role
from ..db import db
from ..handle_files import save_file
from ..models import Block

block_bp = Blueprint('blocks', __name__, template_folder="templates", static_folder="static")


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

@block_bp.after_request
def add_total_blocks_header(response):
    """Append the total number of blocks to every response as a custom header."""
    response.headers['X-Total-Blocks'] = Block.query.count()
    return response


def load_block(f):
    """
    Decorator that resolves `block_id` from URL kwargs into a Block ORM object.

    Pops `block_id` from kwargs, queries the database, and injects the resulting
    `block` instance. Aborts with 404 if the block does not exist.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        block_id = kwargs.pop('block_id', None)
        if block_id is not None:
            block = Block.query.get(block_id)
            if block is None:
                abort(404)
            kwargs['block'] = block
        return f(*args, **kwargs)
    return decorated_function


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@block_bp.route('/', methods=['GET'])
@check_session
@check_role
def get_blocks():
    """List all bouldering blocks."""
    blocks = Block.query.all()
    return render_template('blocks/blocks_list.html', blocks=blocks)


@block_bp.route('/new', methods=['GET'])
@check_session
@check_role
def new_block():
    """Render the form to create a new block."""
    return render_template('blocks/block_new.html')


@block_bp.route('/', methods=['POST'])
@check_session
@check_role
@save_file
def create_block(picture=None):
    """
    Persist a new Block from the submitted form data.

    The optional `picture` argument is injected by the `save_file` decorator.
    """
    block = Block(
        name=request.form['name'],
        grade=request.form['grade'],
        color=request.form['color'],
        sector=request.form['sector'],
        height=float(request.form['height']),
        city=request.form['city'],
        active=True,
        picture=picture,
        description=request.form['description'],
    )
    db.session.add(block)
    db.session.commit()
    return redirect("/blocks")


@block_bp.route('/<int:block_id>')
@check_session
@check_role
@load_block
def get_block_by_id(block):
    """Render the detail page for a single block."""
    return render_template('blocks/block_detail.html', block=block)


@block_bp.route('/<int:block_id>/edit', methods=['GET'])
@check_session
@check_role
@load_block
def edit_block(block):
    """Render the edit form for an existing block."""
    return render_template('blocks/block_edit.html', block=block)


@block_bp.route('/<int:block_id>/edit', methods=['POST'])
@check_session
@check_role
@load_block
@save_file
def update_block(block, picture=None):
    """
    Update an existing Block with the submitted form data.

    Only replaces the picture if a new file was uploaded.
    """
    block.name        = request.form['name']
    block.grade       = request.form['grade']
    block.color       = request.form['color']
    block.sector      = request.form['sector']
    block.height      = float(request.form['height'])
    block.city        = request.form['city']
    block.description = request.form['description']
    if picture:
        block.picture = picture
    db.session.commit()
    return redirect(f"/blocks/{block.id}")


@block_bp.route('/<int:block_id>/delete', methods=['POST'])
@check_session
@check_role
@load_block
def delete_block(block):
    """Delete an existing Block from the database."""
    db.session.delete(block)
    db.session.commit()
    return redirect("/blocks")
