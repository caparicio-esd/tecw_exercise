from functools import wraps

from flask import session, redirect, abort, request


def check_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


permissions = {
    "admin": [
        # Permisos de Vías
        "ways.get_ways",
        "ways.new_way",
        "ways.create_way",
        "ways.get_way_by_id",
        "ways.edit_way",
        "ways.update_way",
        "ways.delete_way",

        # Permisos de Bloques
        "blocks.get_blocks",
        "blocks.new_block",
        "blocks.create_block",
        "blocks.get_block_by_id",
        "blocks.edit_block",
        "blocks.update_block",
        "blocks.delete_block",

        # Permisos de Usuarios
        "users.get_users",
        "users.new_user",
        "users.create_user",
        "users.get_user_by_id",
        "users.edit_user",
        "users.update_user",
        "users.delete_user"
    ],
    "user": [
        "ways.get_ways",
        "ways.get_way_by_id",
        "blocks.get_blocks",
        "blocks.get_block_by_id",

        # ABAC filtering
        "users.get_user_by_id",
        "users.edit_user",
        "users.update_user",
        "users.delete_user"
    ]
}


def check_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            abort(401)

        endpoint = request.endpoint
        role = session["user"]["role"]

        if endpoint not in permissions.get(role, []):
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def check_self(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = session["user"]["role"]
        session_user_id = session["user"]["id"]

        if role == "admin":
            return f(*args, **kwargs)

        target_user_id = kwargs.get('users_id')

        if target_user_id is not None and target_user_id != session_user_id:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def check_role_or_self(f):
    """Permite el acceso si es admin O si el usuario es el propio dueño del recurso."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user")
        if not user:
            abort(401)

        if user["role"] == "admin":
            return f(*args, **kwargs)

        target_user_id = kwargs.get('users_id')
        if target_user_id is not None and target_user_id == user["id"]:
            return f(*args, **kwargs)

        abort(403)

    return decorated_function