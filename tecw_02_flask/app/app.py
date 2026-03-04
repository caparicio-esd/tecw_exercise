from flask import Flask, render_template
from .blueprints import block_bp, users_bp, way_bp, common_bp


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.register_blueprint(block_bp, url_prefix="/blocks")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(way_bp, url_prefix="/ways")
app.register_blueprint(common_bp, url_prefix="/")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)