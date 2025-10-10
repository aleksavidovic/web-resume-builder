from functools import wraps
from flask import flash, render_template, url_for, redirect
from flask_login import current_user, login_required

from ..models import ResumeTheme
from . import admin_bp 
from .forms import ThemeForm
from ..extensions import db

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("The requested page is accessible only to administrator.")
            return redirect(url_for('main.index'))
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
    return render_template("/admin/themes/edit_theme.html", form=form, theme_id=theme_id)


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
        return redirect(url_for('admin.list_themes'))
