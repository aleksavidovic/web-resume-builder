from functools import wraps
from flask import flash, render_template, url_for, redirect
from flask_login import current_user, login_required

from ..models import ResumeTheme, InviteCode, User
from . import admin_bp
from .forms import ThemeForm, CreateInviteCodeForm
from ..extensions import db


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("The requested page is accessible only to administrator.")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/")
@login_required
@admin_required
def admin_home():
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    total_resumes = BuiltResume.query.count()
    total_users = User.query.count()
    analytics = {
        "total_resumes": total_resumes
    }
    return render_template("/admin/dashboard/dashboard.html")


@admin_bp.route("/list_themes", methods=["GET"])
@login_required
@admin_required
def list_themes():
    themes = ResumeTheme.query.all()
    return render_template("/admin/themes/list_themes.html", themes=themes)


@admin_bp.route("/create_theme", methods=["GET", "POST"])
@login_required
@admin_required
def create_theme():
    form = ThemeForm()
    if form.validate_on_submit():
        try:
            new_theme = ResumeTheme()
            form.populate_obj(new_theme)
            db.session.add(new_theme)
            db.session.commit()
            flash("New theme added.", "success")
        except Exception as e:
            flash(f"Error while adding new theme: {e}.", "danger")
        finally:
            return redirect(url_for("admin.list_themes"))
    return render_template("/admin/themes/create_theme.html", form=form)


@admin_bp.route("/themes/<string:theme_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_theme(theme_id):
    theme_to_edit = ResumeTheme.query.filter_by(id=theme_id).first_or_404()
    form = ThemeForm(obj=theme_to_edit)
    if form.validate_on_submit():
        try:
            form.populate_obj(theme_to_edit)
            db.session.commit()
            flash("Theme updated.", "success")
        except Exception as e:
            flash(f"Error while editing theme: {e}.", "danger")
        finally:
            return redirect(url_for("admin.list_themes"))
    return render_template(
        "/admin/themes/edit_theme.html", form=form, theme_id=theme_id
    )


@admin_bp.route("/themes/<string:theme_id>/delete", methods=["GET"])
@login_required
@admin_required
def delete_theme(theme_id):
    try:
        theme_to_delete = ResumeTheme.query.filter_by(id=theme_id).first_or_404()
        db.session.delete(theme_to_delete)
        db.session.commit()
        flash("Theme deleted.", "success")
    except Exception as e:
        flash(f"Error while deleting theme: {e}.", "success")
    finally:
        return redirect(url_for("admin.list_themes"))


@admin_bp.route("/invite_codes", methods=["GET"])
@login_required
@admin_required
def list_invite_codes():
    inv_codes = InviteCode.query.all()
    return render_template("/admin/invite_codes/list_invite_codes.html", invite_codes=inv_codes)


@admin_bp.route("/invite_codes/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_invite_code():
    form = CreateInviteCodeForm()
    if form.validate_on_submit():
        existing_code = InviteCode.query.filter_by(code=form.code.data).first()
        if existing_code:
            flash("Code already exists.", "danger")
            return redirect(url_for("admin.list_invite_codes"))
        new_code = InviteCode()
        form.populate_obj(new_code)
        db.session.add(new_code)
        db.session.commit()
        flash("Code added.", "success")
        return redirect(url_for("admin.list_invite_codes"))
    return render_template("/admin/invite_codes/create_invite_code.html", form=form)


@admin_bp.route("/invite_codes/<string:code_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_invite_code(code_id):
    code_to_delete = InviteCode.query.filter_by(id=code_id).first_or_404()
    db.session.delete(code_to_delete)
    db.session.commit()
    return redirect(url_for("admin.list_invite_codes"))


@admin_bp.route("/users", methods=["GET"])
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template("/admin/users/list_users.html", users=users)
