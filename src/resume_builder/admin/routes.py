from flask import render_template
from . import admin_bp

@admin_bp.route("/list_themes", methods=["GET"])
def list_themes():
    return render_template("/admin/list_themes.html")
