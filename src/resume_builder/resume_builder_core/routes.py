from . import resume_bp
from flask import render_template
from flask_login import login_required

@login_required
@resume_bp.route("/", methods=["GET", "POST"])
def home():
    return render_template("resume_core/home.html")
