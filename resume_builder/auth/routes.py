from .forms import LoginForm
from . import auth_bp
from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from .forms import RegistrationForm
from ..models import User
from .. import db


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(username=form.username.data).first()
        if existing:
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.register"))
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Register", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                flash("Login successful")
                login_user(user, remember=form.remember.data)
                return redirect(url_for("main.index"))
    return render_template("auth/login.html", title="Login", form=form)


@login_required
@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logout successful.")
    return redirect(url_for("main.index"))
