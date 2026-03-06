"""
handle_files.py — File upload decorator.

Provides `save_file`, a route decorator that intercepts the `picture` field
from a multipart form submission, validates its extension, generates a unique
filename, persists the file to disk, and injects the filename as a `picture`
keyword argument into the decorated view function.
"""

import os
import uuid
from functools import wraps

from flask import request, redirect

UPLOAD_FOLDER = 'tecw_02_flask/app/public/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """Return True if *filename* has an allowed image extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(f):
    """
    Decorator that handles the `picture` file upload for a route.

    If the request contains a valid image file under the `picture` key:
      1. Validates the file extension against ALLOWED_EXTENSIONS.
      2. Generates a UUID-based filename to avoid collisions.
      3. Creates the upload directory if it does not exist.
      4. Saves the file to UPLOAD_FOLDER.
      5. Passes the new filename as `picture` to the wrapped view.

    If no file is uploaded, `picture=None` is passed instead.
    If the file extension is invalid, the request is redirected back to its URL.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        file = request.files.get('picture')
        kwargs['picture'] = None

        if file and file.filename:
            if not allowed_file(file.filename):
                return redirect(request.url)

            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            kwargs['picture'] = filename

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        return f(*args, **kwargs)
    return decorated_function
