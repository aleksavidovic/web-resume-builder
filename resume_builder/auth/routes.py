from .forms import LoginForm
from . import auth_bp
from flask import render_template, url_for, redirect, flash, current_app
from flask_login import current_user, login_required, login_user, logout_user
from .forms import RegistrationForm, RegistrationWithInviteCodeForm
from ..decorators import anonymous_user_required, feature_flag_required
from .services import AuthenticationService
from .exceptions import UserNotFoundError, IncorrectPasswordError, UserAlreadyExistsError, InviteCodeRedeemedError, InviteCodeNotFoundError
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
        try:
            auth_service = AuthenticationService(db.session)
            auth_service.register_user_with_invite_code(form.data)
        except InviteCodeNotFoundError:
            flash("Invalid Invitation Code.", "danger")
            return redirect(url_for("auth.register_with_invite_code"))
        except InviteCodeRedeemedError:
            flash("Invitation Code already redeemed.", "danger")
            return redirect(url_for("auth.register_with_invite_code"))
        except UserAlreadyExistsError as e:
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.register_with_invite_code"))
        else:
            flash("Your account has been created! You can now log in.", "success")
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
            auth_service = AuthenticationService(db.session)
            auth_service.login(form.data)
        except IncorrectPasswordError:
            flash("Incorrect password.", "danger")
            return render_template("auth/login.html", title="Login", form=form)
        except UserNotFoundError:
            flash("No account exists with the provided username.", "danger")
            return render_template("auth/login.html", title="Login", form=form)
        except Exception as e:
            flash(f"Unexpected Error while trying to log in: {e}")
            return render_template("auth/login.html", title="Login", form=form)
        else:
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
    return render_template("auth/login.html", title="Login", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful.")
    return redirect(url_for("main.index"))
