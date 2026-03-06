from flask import Blueprint, render_template, request, flash, redirect, session

from ..db import db
from ..models import User

auth_bp = Blueprint('auth', __name__, template_folder="templates")


@auth_bp.route('/register', methods=['GET'])
def register_view():
    return render_template('auth/register.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    level = request.form['level']
    member_since = request.form['member_since']
    city = request.form['city']

    if User.query.filter_by(email=email).first():
        flash('El email ya está registrado.')
        return redirect('/auth/register')

    new_user = User(name=name, email=email, level=level, member_since=member_since, sessions=0, active=True, city=city)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('Registro exitoso, ahora puedes iniciar sesión.')
    return redirect('/')


@auth_bp.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user'] = {
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'id': user.id
        }
        flash('Inicio de sesión exitoso.')
        return redirect('/')
    else:
        flash('Correo o contraseña incorrectos.')
        return redirect('/auth/login')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada correctamente.')
    return redirect('/')
