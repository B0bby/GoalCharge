from flask import (current_app, render_template)

def init(app):
    @app.route("/")
    def index():
        return render_template("index.html")
