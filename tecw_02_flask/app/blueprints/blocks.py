import flask
from flask import Blueprint, render_template, redirect, request
from ..data import BLOCKS
from ..handle_files import save_file

block_bp = Blueprint('blocks', __name__, template_folder="templates", static_folder="static")


@block_bp.route('/', methods=['GET'])
def get_blocks():
    return render_template('blocks/blocks_list.html', blocks=BLOCKS)


@block_bp.route('/new', methods=['GET'])
def new_block():
    return render_template('blocks/block_new.html')


@block_bp.route('/', methods=['POST'])
@save_file
def create_block(picture=None):
    new_id = max(b['id'] for b in BLOCKS) + 1
    BLOCKS.append({
        "id":          new_id,
        "name":        request.form['name'],
        "grade":       request.form['grade'],
        "color":       request.form['color'],
        "sector":      request.form['sector'],
        "height":      float(request.form['height']),
        "city":        request.form['city'],
        "active":      True,
        "picture":     picture,
        "description": request.form['description'],
    })
    return redirect("/blocks")


@block_bp.route('/<int:block_id>')
def get_block_by_id(block_id):
    block = next((b for b in BLOCKS if b['id'] == block_id), None)
    if block is None:
        return render_template('404.html'), 404
    return render_template('blocks/block_detail.html', block=block)


@block_bp.route('/<int:block_id>/edit', methods=['GET'])
def edit_block(block_id):
    block = next((b for b in BLOCKS if b['id'] == block_id), None)
    if block is None:
        return render_template('404.html'), 404
    return render_template('blocks/block_edit.html', block=block)


@block_bp.route('/<int:block_id>/edit', methods=['POST'])
@save_file
def update_block(block_id, picture=None):
    idx = next((i for i, b in enumerate(BLOCKS) if b['id'] == block_id), None)
    if idx is None:
        return render_template('404.html'), 404
    BLOCKS[idx].update({
        "name":        request.form['name'],
        "grade":       request.form['grade'],
        "color":       request.form['color'],
        "sector":      request.form['sector'],
        "height":      float(request.form['height']),
        "city":        request.form['city'],
        "description": request.form['description'],
    })
    if picture:
        BLOCKS[idx]['picture'] = picture
    return redirect(f"/blocks/{block_id}")


@block_bp.route('/<int:block_id>/delete', methods=['POST'])
def delete_block(block_id):
    idx = next((i for i, b in enumerate(BLOCKS) if b['id'] == block_id), None)
    if idx is not None:
        BLOCKS.pop(idx)
    return redirect("/blocks")
