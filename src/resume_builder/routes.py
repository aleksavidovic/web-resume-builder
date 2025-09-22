from flask import Blueprint, render_template

main_bp = Blueprint(name="main", import_name=__name__)


@main_bp.route("/")
def index():
    return render_template("home.html")

@main_bp.route("/my_resume")
def my_resume():
    return "<h1>My Resume</h1>"


@main_bp.route("/about")
def about():
    return "<h1>About</h1>"

@main_bp.route("/contact")
def contact():
    return "<h1>Contact</h1>"

def register():
    return render_template("register.html")

def login():
    return render_template("login.html")

def logout():
    return render_template("logout.html")
