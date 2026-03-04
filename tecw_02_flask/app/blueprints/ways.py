from flask import Blueprint, render_template
from ..data import WAYS

way_bp = Blueprint('ways', __name__, template_folder="templates", static_folder="static")


@way_bp.route('/')
def get_ways():
    return render_template('ways/ways_list.html', ways=WAYS)


@way_bp.route('/<int:way_id>')
def get_way_by_id(way_id):
    way = next((w for w in WAYS if w['id'] == way_id), None)
    if way is None:
        return render_template('404.html'), 404
    return render_template('ways/way_detail.html', way=way)
