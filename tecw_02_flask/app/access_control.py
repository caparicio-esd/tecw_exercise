"""
access_control.py — Authentication and authorisation decorators.

Provides route decorators that enforce:
  - Session presence (check_session)
  - Role-based access control via a permission table (check_role)
  - Object-level ownership checks (check_self)
  - Combined role-or-ownership check (check_role_or_self)
"""

from functools import wraps

from flask import session, abort, request


# ---------------------------------------------------------------------------
# Permission table
# Maps each role to the list of endpoint names it is allowed to access.
# Endpoint names follow the pattern  "<blueprint_name>.<view_function_name>".
# ---------------------------------------------------------------------------

permissions = {
    "admin": [
        # Ways
        "ways.get_ways",
        "ways.new_way",
        "ways.create_way",
        "ways.get_way_by_id",
        "ways.edit_way",
        "ways.update_way",
        "ways.delete_way",
        # Blocks
        "blocks.get_blocks",
        "blocks.new_block",
        "blocks.create_block",
        "blocks.get_block_by_id",
        "blocks.edit_block",
        "blocks.update_block",
        "blocks.delete_block",
        # Users
        "users.get_users",
        "users.new_user",
        "users.create_user",
        "users.get_user_by_id",
        "users.edit_user",
        "users.update_user",
        "users.delete_user",
    ],
    "user": [
        # Read-only access to ways and blocks
        "ways.get_ways",
        "ways.get_way_by_id",
        "blocks.get_blocks",
        "blocks.get_block_by_id",
        # Own profile management (further filtered by check_self / check_role_or_self)
        "users.get_user_by_id",
        "users.edit_user",
        "users.update_user",
        "users.delete_user",
    ],
}


def check_session(f):
    """Abort with 403 if there is no authenticated user in the session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def check_role(f):
    """
    Abort with 403 if the current user's role does not have permission
    to access the requested endpoint, as defined in the permissions table.
    """
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
    """
    Allow access only if the current user is an admin OR if the target
    resource belongs to the current user (identified by `users_id` in kwargs).
    """
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
    """
    Allow access if the current user is an admin OR if the target resource
    belongs to the current user. Unlike check_role + check_self, this
    decorator grants access without requiring the endpoint to be listed in
    the permissions table — useful for self-service routes (edit/delete own profile).
    """
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
