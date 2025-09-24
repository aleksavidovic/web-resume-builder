from flask import Blueprint, render_template

main_bp = Blueprint(name="main", import_name=__name__)


@main_bp.route("/")
def index():
    return render_template("home.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact")
def contact():
    return "<h1>Contact</h1>"

