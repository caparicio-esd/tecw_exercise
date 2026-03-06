from functools import wraps

from flask import Blueprint, render_template, redirect, request, abort, session, flash

from ..access_control import check_session, check_role, check_self, check_role_or_self
from ..db import db
from ..handle_files import save_file
from ..models import User

users_bp = Blueprint('users', __name__, template_folder="templates", static_folder="static")


# ===================================
# Middleware
# ===================================

@users_bp.after_request
def add_total_users_header(response):
    response.headers['X-Total-Users'] = User.query.count()
    return response


def load_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        users_id = kwargs.pop('users_id', None)
        if users_id is not None:
            user = User.query.get(users_id)
            if user is None:
                abort(404)
            kwargs['user'] = user
        return f(*args, **kwargs)
    return decorated_function


# ===================================
# Rutas
# ===================================

@users_bp.route('/', methods=['GET'])
@check_session
def get_users():
    users = User.query.all()
    return render_template('users/users_list.html', users=users)


@users_bp.route('/new', methods=['GET'])
@check_session
@check_role
def new_user():
    return render_template('users/user_new.html')


@users_bp.route('/', methods=['POST'])
@check_session
@check_role
@save_file
def create_user(picture=None):
    user = User(
        name=request.form['name'],
        email=request.form['email'],
        avatar=request.form['avatar'],
        level=request.form['level'],
        city=request.form['city'],
        member_since=request.form['member_since'],
        sessions=0,
        active=True,
        picture=picture,
    )
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@users_bp.route('/<int:users_id>')
@check_session
@load_user
def get_user_by_id(user):
    return render_template('users/user_detail.html', user=user)


@users_bp.route('/<int:users_id>/edit', methods=['GET'])
@check_session
@check_role_or_self
@load_user
def edit_user(user):
    return render_template('users/user_edit.html', user=user)


@users_bp.route('/<int:users_id>/edit', methods=['POST'])
@check_session
@check_role_or_self
@load_user
@save_file
def update_user(user, picture=None):
    user.name         = request.form['name']
    user.email        = request.form['email']
    user.avatar       = request.form['avatar']
    user.level        = request.form['level']
    user.city         = request.form['city']
    user.member_since = request.form['member_since']
    if picture:
        user.picture = picture
    db.session.commit()
    return redirect(f"/users/{user.id}")


@users_bp.route('/<int:users_id>/delete', methods=['POST'])
@check_session
@check_role_or_self
@load_user
def delete_user(user):
    if session['user']['id'] == user.id and session['user']['role'] == 'admin':
        flash("Un administrador no puede eliminarse a sí mismo.", "error")
        return redirect(f"/users/{user.id}")
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
