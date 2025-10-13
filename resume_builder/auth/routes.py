from .forms import LoginForm
from . import auth_bp
from flask import render_template, url_for, redirect, flash, current_app
from flask_login import current_user, login_required, login_user, logout_user
from .forms import RegistrationForm, RegistrationWithInviteCodeForm
from ..models import User, InviteCode
from .. import db


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if not current_app.config["FEATURE_FLAGS"]["registration_enabled"]:
        flash("Registration is currently disabled.", "danger")
        return redirect(url_for("main.index"))
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


@auth_bp.route("/register_with_invite_code", methods=["GET", "POST"])
def register_with_invite_code():
    if not current_app.config["FEATURE_FLAGS"]["register_with_invite_code"]:
        flash("Registration with Invite Code is currently disabled.", "danger")
        return redirect(url_for("main.index"))
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationWithInviteCodeForm()

    if form.validate_on_submit():
        invite_code = InviteCode.query.filter_by(code=form.invite_code.data).first()
        if not invite_code:
            flash("Invalid Invitation Code.", "danger")
            return redirect(url_for("auth.register_with_invite_code"))
        if invite_code.redeemed:
            flash("Invitation Code already redeemed.", "danger")
            return redirect(url_for("auth.register_with_invite_code"))
        existing = User.query.filter_by(username=form.username.data).first()

        if existing:
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.register_with_invite_code"))

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        invite_code.redeemed = True
        invite_code.user = user
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("auth.login"))
    return render_template(
        "auth/register_with_invite_code.html",
        title="Register using Invitation Code",
        form=form,
    )


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
