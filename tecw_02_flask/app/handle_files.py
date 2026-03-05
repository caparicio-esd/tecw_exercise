import os
import uuid
from functools import wraps
from flask import request, redirect
from app import app

app.config['UPLOAD_FOLDER'] = 'app/assets/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        file = request.files['file'] if 'file' in request.files else None # Comprueba si se ha subido un fichero
        kwargs['filename'] = None
        if file:
            if not allowed_file(file.filename): # Comprueba si la extensión del fichero es permitida
                return redirect(request.url)
            filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}" if file else None # Genera un nombre único para el fichero
            kwargs['filename'] = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Guarda el fichero en la carpeta de imágenes usando la libreria os
        return f(*args, **kwargs)
    return decorated_function