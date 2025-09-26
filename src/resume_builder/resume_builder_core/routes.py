from resume_builder.resume_builder_core.forms import BasicInfoForm
from . import resume_bp
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from ..models import BasicInfo, Summary
from .. import db
from werkzeug.exceptions import NotFound

@login_required
@resume_bp.route("/", methods=["GET", "POST"])
def home():
    basic_info = BasicInfo.query.filter_by(user_id=current_user.id).all()
    summaries = Summary.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/home.html", basic_info=basic_info, summaries=summaries)

@login_required
@resume_bp.route("/basic_info", methods=["GET", "POST"])
def basic_info():
    users_basic_info = BasicInfo.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/basic_info.html", basic_infos=users_basic_info)

@login_required
@resume_bp.route("/basic_info/<int:info_id>/edit", methods=["GET", "POST"])
def edit_basic_info(info_id):
    """
    Handles editing an existing BasicInfo entry.
    """
    # Query for the specific BasicInfo object or raise a 404 error.
    # The filter also ensures a user can only edit their own entries.
    info_to_edit = BasicInfo.query.filter_by(id=info_id, user_id=current_user.id).first()
    if not info_to_edit:
        raise NotFound()

    form = BasicInfoForm(obj=info_to_edit)

    if form.validate_on_submit():
        try:
            # Update the object's attributes from the submitted form data
            form.populate_obj(info_to_edit)
            db.session.commit()
            flash("Your 'Basic Info' section has been updated!", "success")
            return redirect(url_for("resume.basic_info"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating: {e}", "danger")

    # For a GET request, render the template with the pre-filled form
    return render_template("resume_core/edit_basic_info.html", form=form, info_id=info_id)

@login_required
@resume_bp.route("/basic_info/create", methods=["GET", "POST"])
def create_basic_info():
    form = BasicInfoForm()
    if form.validate_on_submit():
        print("Form submitted for validation")
        try:
            full_name = form.full_name.data
            job_title = form.job_title.data
            address = form.address.data
            contact_email = form.contact_email.data
            contact_phone = form.contact_phone.data
            linkedin_url = form.linkedin_url.data
            github_url = form.github_url.data
            new_basic_info = BasicInfo( full_name=full_name, 
                                        job_title=job_title, 
                                        address=address,     
                                        contact_email=contact_email, 
                                        contact_phone=contact_phone, 
                                        linkedin_url=linkedin_url,   
                                        github_url=github_url,
                                        user_id=current_user.id)
            db.session.add(new_basic_info)
            db.session.commit()
            flash("New Basic Info Created!", "success")
            return(redirect(url_for("resume.basic_info")))
        except Exception as e:
            flash(f"Error while saving Basic Info: {e}")
            return(redirect(url_for("resume.create_basic_info")))
        
    return render_template("resume_core/create_basic_info.html", form=form)
