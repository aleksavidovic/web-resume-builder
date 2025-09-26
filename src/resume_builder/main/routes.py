from flask import render_template
from . import main_bp


@main_bp.route("/")
def index():
    return render_template("main/home.html")


@main_bp.route("/about")
def about():
    return render_template("main/about.html")
