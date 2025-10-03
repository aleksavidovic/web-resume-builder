from flask import flash, render_template, url_for, redirect

from ..models import ResumeTheme
from . import admin_bp 
from .forms import ThemeForm
from ..extensions import db

@admin_bp.route("/list_themes", methods=["GET"])
def list_themes():
    themes = ResumeTheme.query.all()
    return render_template("/admin/list_themes.html", themes=themes)


@admin_bp.route("/create_theme", methods=["GET", "POST"])
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
    return render_template("/admin/create_theme.html", form=form)

@admin_bp.route("/themes/<string:theme_id>/delete", methods=["GET"])
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
