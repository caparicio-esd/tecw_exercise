import os
import uuid
from functools import wraps
from flask import request, redirect, current_app

UPLOAD_FOLDER = 'tecw_02_flask/app/public/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        file = request.files['picture'] if 'picture' in request.files else None # Comprueba si se ha subido un fichero
        print(file)
        kwargs['picture'] = None
        if file:
            if not allowed_file(file.filename): # Comprueba si la extensión del fichero es permitida
                return redirect(request.url)
            filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}" if file else None # Genera un nombre único para el fichero
            kwargs['picture'] = filename
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename)) # Guarda el fichero en la carpeta de imágenes usando la libreria os
        return f(*args, **kwargs)
    return decorated_function