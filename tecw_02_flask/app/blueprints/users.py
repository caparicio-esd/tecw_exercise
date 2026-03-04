from flask import Blueprint, render_template
from ..data import USERS

users_bp = Blueprint('users', __name__, template_folder="templates", static_folder="static")


@users_bp.route('/')
def get_users():
    return render_template('users/users_list.html', users=USERS)


@users_bp.route('/<int:users_id>')
def get_user_by_id(users_id):
    user = next((u for u in USERS if u['id'] == users_id), None)
    if user is None:
        return render_template('404.html'), 404
    return render_template('users/user_detail.html', user=user)
