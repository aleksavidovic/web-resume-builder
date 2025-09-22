from . import auth_bp
from flask import render_template

@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")

@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    return render_template("auth/logout.html")
