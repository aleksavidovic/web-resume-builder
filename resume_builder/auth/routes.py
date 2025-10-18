from .forms import LoginForm
from . import auth_bp
from flask import render_template, url_for, redirect, flash, current_app
from flask_login import current_user, login_required, login_user, logout_user
from .forms import RegistrationForm, RegistrationWithInviteCodeForm
from ..decorators import anonymous_user_required, feature_flag_required
from .services import AuthenticationService
from .exceptions import UserNotFoundError
from ..models import User, InviteCode
from .. import db


@auth_bp.route("/register", methods=["GET", "POST"])
@feature_flag_required("registration_enabled")
@anonymous_user_required
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            auth_service = AuthenticationService(db.session)
            auth_service.register_user(form.data)
        except UserAlreadyExistsError:
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.register"))
        else:
            flash("Your account has been created! You can now log in", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Register", form=form)


@auth_bp.route("/register_with_invite_code", methods=["GET", "POST"])
@feature_flag_required("register_with_invite_code")
@anonymous_user_required
def register_with_invite_code():
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
@anonymous_user_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.check_password(form.password.data):
                    flash("Login successful")
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for("main.index"))
            else:
                raise UserNotFoundError(
                    f"No user found with username: {form.username.data}"
                )
        except Exception as e:
            flash(f"Error while trying to log in: {e}")
            return render_template("auth/login.html", title="Login", form=form)
    return render_template("auth/login.html", title="Login", form=form)


@login_required
@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logout successful.")
    return redirect(url_for("main.index"))
