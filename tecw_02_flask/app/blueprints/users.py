from flask import Blueprint, render_template, redirect, request
from ..data import USERS
from ..handle_files import save_file

users_bp = Blueprint('users', __name__, template_folder="templates", static_folder="static")


@users_bp.route('/', methods=['GET'])
def get_users():
    return render_template('users/users_list.html', users=USERS)


@users_bp.route('/new', methods=['GET'])
def new_user():
    return render_template('users/user_new.html')


@users_bp.route('/', methods=['POST'])
@save_file
def create_user(picture=None):
    new_id = max(u['id'] for u in USERS) + 1
    USERS.append({
        "id":           new_id,
        "name":         request.form['name'],
        "email":        request.form['email'],
        "avatar":       request.form['avatar'],
        "level":        request.form['level'],
        "city":         request.form['city'],
        "member_since": request.form['member_since'],
        "sessions":     0,
        "active":       True,
        "picture":      picture,
    })
    return redirect("/users")


@users_bp.route('/<int:users_id>')
def get_user_by_id(users_id):
    user = next((u for u in USERS if u['id'] == users_id), None)
    if user is None:
        return render_template('404.html'), 404
    return render_template('users/user_detail.html', user=user)


@users_bp.route('/<int:users_id>/edit', methods=['GET'])
def edit_user(users_id):
    user = next((u for u in USERS if u['id'] == users_id), None)
    if user is None:
        return render_template('404.html'), 404
    return render_template('users/user_edit.html', user=user)


@users_bp.route('/<int:users_id>/edit', methods=['POST'])
@save_file
def update_user(users_id, picture=None):
    idx = next((i for i, u in enumerate(USERS) if u['id'] == users_id), None)
    if idx is None:
        return render_template('404.html'), 404
    USERS[idx].update({
        "name":         request.form['name'],
        "email":        request.form['email'],
        "avatar":       request.form['avatar'],
        "level":        request.form['level'],
        "city":         request.form['city'],
        "member_since": request.form['member_since'],
        "picture":      picture,
    })
    return redirect(f"/users/{users_id}")


@users_bp.route('/<int:users_id>/delete', methods=['POST'])
def delete_user(users_id):
    idx = next((i for i, u in enumerate(USERS) if u['id'] == users_id), None)
    if idx is not None:
        USERS.pop(idx)
    return redirect("/users")
