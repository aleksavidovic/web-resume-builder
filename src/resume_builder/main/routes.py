from flask import render_template
from flask_login import login_required
from . import main_bp


@login_required
@main_bp.route("/")
def index():
    return render_template("home.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")
