from functools import wraps

from flask import Blueprint, render_template, redirect, request, abort

from ..access_control import check_role
from ..db import db
from ..handle_files import save_file
from ..models import Block

block_bp = Blueprint('blocks', __name__, template_folder="templates", static_folder="static")


# ===================================
# Middleware
# ===================================

@block_bp.after_request
def add_total_blocks_header(response):
    response.headers['X-Total-Blocks'] = Block.query.count()
    return response


def load_block(f):
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


# ===================================
# Rutas
# ===================================

@block_bp.route('/', methods=['GET'])
@check_role
def get_blocks():
    blocks = Block.query.all()
    return render_template('blocks/blocks_list.html', blocks=blocks)


@block_bp.route('/new', methods=['GET'])
@check_role
def new_block():
    return render_template('blocks/block_new.html')


@block_bp.route('/', methods=['POST'])
@check_role
@save_file
def create_block(picture=None):
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
@check_role
@load_block
def get_block_by_id(block):
    return render_template('blocks/block_detail.html', block=block)


@block_bp.route('/<int:block_id>/edit', methods=['GET'])
@check_role
@load_block
def edit_block(block):
    return render_template('blocks/block_edit.html', block=block)


@block_bp.route('/<int:block_id>/edit', methods=['POST'])
@check_role
@load_block
@save_file
def update_block(block, picture=None):
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
@check_role
@load_block
def delete_block(block):
    db.session.delete(block)
    db.session.commit()
    return redirect("/blocks")
