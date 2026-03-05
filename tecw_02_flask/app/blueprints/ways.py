from flask import Blueprint, render_template, redirect, request
from ..data import WAYS

way_bp = Blueprint('ways', __name__, template_folder="templates", static_folder="static")


@way_bp.route('/', methods=['GET'])
def get_ways():
    return render_template('ways/ways_list.html', ways=WAYS)


@way_bp.route('/new', methods=['GET'])
def new_way():
    return render_template('ways/way_new.html')


@way_bp.route('/', methods=['POST'])
def create_way():
    new_id = max(w['id'] for w in WAYS) + 1
    WAYS.append({
        "id":          new_id,
        "name":        request.form['name'],
        "grade":       request.form['grade'],
        "type":        request.form['type'],
        "length":      int(request.form['length']),
        "city":        request.form['city'],
        "active":      True,
        "description": request.form['description'],
    })
    return redirect("/ways")


@way_bp.route('/<int:way_id>')
def get_way_by_id(way_id):
    way = next((w for w in WAYS if w['id'] == way_id), None)
    if way is None:
        return render_template('404.html'), 404
    return render_template('ways/way_detail.html', way=way)


@way_bp.route('/<int:way_id>/edit', methods=['GET'])
def edit_way(way_id):
    way = next((w for w in WAYS if w['id'] == way_id), None)
    if way is None:
        return render_template('404.html'), 404
    return render_template('ways/way_edit.html', way=way)


@way_bp.route('/<int:way_id>/edit', methods=['POST'])
def update_way(way_id):
    idx = next((i for i, w in enumerate(WAYS) if w['id'] == way_id), None)
    if idx is None:
        return render_template('404.html'), 404
    WAYS[idx].update({
        "name":        request.form['name'],
        "grade":       request.form['grade'],
        "type":        request.form['type'],
        "length":      int(request.form['length']),
        "city":        request.form['city'],
        "description": request.form['description'],
    })
    return redirect(f"/ways/{way_id}")


@way_bp.route('/<int:way_id>/delete', methods=['POST'])
def delete_way(way_id):
    idx = next((i for i, w in enumerate(WAYS) if w['id'] == way_id), None)
    if idx is not None:
        WAYS.pop(idx)
    return redirect("/ways")
