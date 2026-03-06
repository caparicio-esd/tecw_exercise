from functools import wraps

from flask import Blueprint, render_template, redirect, request, abort

from ..access_control import check_role
from ..db import db
from ..handle_files import save_file
from ..models import Way

way_bp = Blueprint('ways', __name__, template_folder="templates", static_folder="static")


# ===================================
# Middleware
# ===================================

@way_bp.after_request
def add_total_ways_header(response):
    response.headers['X-Total-Ways'] = Way.query.count()
    return response


def load_way(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        way_id = kwargs.pop('way_id', None)  # extrae y elimina way_id de kwargs
        if way_id is not None:
            way = Way.query.get(way_id)
            if way is None:
                abort(404)
            kwargs['way'] = way
        return f(*args, **kwargs)
    return decorated_function


# ===================================
# Rutas
# ===================================

@way_bp.route('/', methods=['GET'])
@check_role
def get_ways():
    ways = Way.query.all()
    return render_template('ways/ways_list.html', ways=ways)


@way_bp.route('/new', methods=['GET'])
@check_role
def new_way():
    return render_template('ways/way_new.html')


@way_bp.route('/', methods=['POST'])
@check_role
@save_file
def create_way(picture=None):
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
@check_role
@load_way
def get_way_by_id(way):
    return render_template('ways/way_detail.html', way=way)


@way_bp.route('/<int:way_id>/edit', methods=['GET'])
@check_role
@load_way
def edit_way(way):
    return render_template('ways/way_edit.html', way=way)


@way_bp.route('/<int:way_id>/edit', methods=['POST'])
@check_role
@load_way
@save_file
def update_way(way, picture=None):
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
@check_role
@load_way
def delete_way(way):
    db.session.delete(way)
    db.session.commit()
    return redirect("/ways")
