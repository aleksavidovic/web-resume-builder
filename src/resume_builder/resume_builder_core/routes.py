from . import resume_bp
from flask import render_template
from flask_login import login_required, current_user
from ..models import BasicInfo, Summary

@login_required
@resume_bp.route("/", methods=["GET", "POST"])
def home():
    basic_info = BasicInfo.query.filter_by(user_id=current_user.id).all()
    summaries = Summary.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/home.html", basic_info=basic_info, summaries=summaries)
