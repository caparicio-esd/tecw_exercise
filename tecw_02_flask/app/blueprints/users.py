"""
blueprints/users.py — CRUD routes for gym members (usuarios).

Access rules:
  - GET /            → any authenticated user (list)
  - GET /<id>        → any authenticated user (detail)
  - POST / (create)  → admin only
  - GET/POST /<id>/edit   → admin OR the user themselves
  - POST /<id>/delete     → admin OR the user themselves
                            (an admin cannot delete their own account)

The `load_user` decorator resolves `users_id` from the URL into a User instance.
After every response, an `X-Total-Users` header is added with the total count.
"""

from functools import wraps

from flask import Blueprint, render_template, redirect, request, abort, session, flash

from ..access_control import check_session, check_role, check_role_or_self
from ..db import db
from ..handle_files import save_file
from ..models import User

users_bp = Blueprint('users', __name__, template_folder="templates", static_folder="static")


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

@users_bp.after_request
def add_total_users_header(response):
    """Append the total number of users to every response as a custom header."""
    response.headers['X-Total-Users'] = User.query.count()
    return response


def load_user(f):
    """
    Decorator that resolves `users_id` from URL kwargs into a User ORM object.

    Pops `users_id` from kwargs, queries the database, and injects the resulting
    `user` instance. Aborts with 404 if the user does not exist.
    """
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


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@users_bp.route('/', methods=['GET'])
@check_session
def get_users():
    """List all registered users. Accessible to any authenticated user."""
    users = User.query.all()
    return render_template('users/users_list.html', users=users)


@users_bp.route('/new', methods=['GET'])
@check_session
@check_role
def new_user():
    """Render the form to create a new user. Admin only."""
    return render_template('users/user_new.html')


@users_bp.route('/', methods=['POST'])
@check_session
@check_role
@save_file
def create_user(picture=None):
    """
    Persist a new User from the submitted form data. Admin only.

    The optional `picture` argument is injected by the `save_file` decorator.
    """
    user = User(
        name=request.form['name'],
        email=request.form['email'],
        avatar=request.form['avatar'],
        level=request.form['level'],
        city=request.form['city'],
        member_since=request.form['member_since'],
        role=request.form.get('role', 'user'),
        sessions=0,
        active=True,
        picture=picture,
    )
    user.set_password(request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@users_bp.route('/<int:users_id>')
@check_session
@load_user
def get_user_by_id(user):
    """Render the profile detail page. Accessible to any authenticated user."""
    return render_template('users/user_detail.html', user=user)


@users_bp.route('/<int:users_id>/edit', methods=['GET'])
@check_session
@check_role_or_self
@load_user
def edit_user(user):
    """Render the edit form for a user profile. Accessible to admins or the user themselves."""
    return render_template('users/user_edit.html', user=user)


@users_bp.route('/<int:users_id>/edit', methods=['POST'])
@check_session
@check_role_or_self
@load_user
@save_file
def update_user(user, picture=None):
    """
    Update a user's profile with the submitted form data.

    Only replaces the password if a non-empty value is provided.
    Only replaces the picture if a new file was uploaded.
    Accessible to admins or the user themselves.
    """
    user.name         = request.form['name']
    user.email        = request.form['email']
    user.avatar       = request.form['avatar']
    user.level        = request.form['level']
    user.city         = request.form['city']
    user.member_since = request.form['member_since']
    user.role         = request.form.get('role', user.role)

    new_password = request.form.get('password')
    if new_password:
        user.set_password(new_password)

    if picture:
        user.picture = picture

    db.session.commit()
    return redirect(f"/users/{user.id}")


@users_bp.route('/<int:users_id>/delete', methods=['POST'])
@check_session
@check_role_or_self
@load_user
def delete_user(user):
    """
    Delete a user account.

    Admins cannot delete their own account; attempting to do so redirects
    back to the profile page with an error flash message.
    """
    if session['user']['id'] == user.id and session['user']['role'] == 'admin':
        flash("An administrator cannot delete their own account.", "error")
        return redirect(f"/users/{user.id}")

    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
