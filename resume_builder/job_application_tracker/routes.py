from flask import render_template
from . import job_app_tracker_bp

@job_app_tracker_bp.route("/")
def home():
    return render_template("job_app_tracker/home.html")
