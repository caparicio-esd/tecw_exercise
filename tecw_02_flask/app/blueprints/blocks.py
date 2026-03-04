from flask import Blueprint, render_template
from ..data import BLOCKS

block_bp = Blueprint('blocks', __name__, template_folder="templates", static_folder="static")


@block_bp.route('/')
def get_blocks():
    return render_template('blocks/blocks_list.html', blocks=BLOCKS)


@block_bp.route('/<int:block_id>')
def get_block_by_id(block_id):
    block = next((b for b in BLOCKS if b['id'] == block_id), None)
    if block is None:
        return render_template('404.html'), 404
    return render_template('blocks/block_detail.html', block=block)
