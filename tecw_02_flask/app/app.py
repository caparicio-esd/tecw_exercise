import logging

from flask import Flask, render_template, request
from .blueprints import block_bp, users_bp, way_bp, common_bp

logging.basicConfig(level=logging.DEBUG)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="public",
    static_url_path=""
)

app.secret_key = '1234'

app.register_blueprint(block_bp, url_prefix="/blocks")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(way_bp, url_prefix="/ways")
app.register_blueprint(common_bp, url_prefix="/")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.before_request
def before_request():
    log = f"Request: {request.method} {request.path}"
    logging.debug(log)


if __name__ == '__main__':
    app.run(debug=True)