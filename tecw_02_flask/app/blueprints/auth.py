"""
blueprints/auth.py — Authentication routes.

Handles user registration, login and logout using Flask sessions.
Passwords are never stored in plain text; the User model hashes them
via werkzeug.security before persisting to the database.
"""

from flask import Blueprint, render_template, request, flash, redirect, session

from ..db import db
from ..models import User

auth_bp = Blueprint('auth', __name__, template_folder="templates")


@auth_bp.route('/register', methods=['GET'])
def register_view():
    """Render the registration form."""
    return render_template('auth/register.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Process the registration form.

    Validates that the e-mail is not already taken, creates a new User,
    hashes the provided password and persists the record. On success the
    user is redirected to the home page with a flash confirmation.
    """
    name         = request.form['name']
    email        = request.form['email']
    password     = request.form['password']
    level        = request.form['level']
    member_since = request.form['member_since']
    city         = request.form['city']

    if User.query.filter_by(email=email).first():
        flash('El email ya está registrado.', 'error')
        return redirect('/auth/register')

    new_user = User(
        name=name,
        email=email,
        level=level,
        member_since=member_since,
        sessions=0,
        active=True,
        city=city,
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash('Registro exitoso, ahora puedes iniciar sesión.', 'success')
    return redirect('/')


@auth_bp.route('/login', methods=['GET'])
def login_view():
    """Render the login form."""
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Process the login form.

    Looks up the user by e-mail and verifies the password hash.
    On success, stores a minimal user dict in the session and redirects home.
    On failure, flashes an error and redirects back to the login page.
    """
    email    = request.form['email']
    password = request.form['password']
    user     = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user'] = {
            'name':   user.name,
            'email':  user.email,
            'role':   user.role,
            'id':     user.id,
            'avatar': user.avatar,
        }
        flash('Inicio de sesión exitoso.', 'success')
        return redirect('/')

    flash('Correo o contraseña incorrectos.', 'error')
    return redirect('/auth/login')


@auth_bp.route('/logout')
def logout():
    """Remove the user from the session and redirect to the home page."""
    session.pop('user', None)
    flash('Sesión cerrada correctamente.', 'success')
    return redirect('/')
