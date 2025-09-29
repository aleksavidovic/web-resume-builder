import uuid
from resume_builder.resume_builder_core.forms import BasicInfoForm, ExperienceForm, SummaryForm
from . import resume_bp
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from ..models import BasicInfo, Education, Summary, Experience
from .. import db
from werkzeug.exceptions import NotFound


@login_required
@resume_bp.route("/", methods=["GET", "POST"])
def home():
    basic_info = BasicInfo.query.filter_by(user_id=current_user.id).all()
    summaries = Summary.query.filter_by(user_id=current_user.id).all()
    experiences = Experience.query.filter_by(user_id=current_user.id).all()
    educations = Education.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "resume_core/home.html", 
        basic_info=basic_info, 
        summaries=summaries, 
        experiences=experiences,
        educations=educations
    )

##########################
######  BASIC INFO  ######
##########################

###########################
## BASIC INFO: LIST VIEW ##
###########################

@login_required
@resume_bp.route("/basic_info_list", methods=["GET", "POST"])
def list_basic_info():
    users_basic_info = BasicInfo.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/basic_info/list_basic_info.html", basic_infos=users_basic_info)


########################
## BASIC INFO: CREATE ##
########################

@login_required
@resume_bp.route("/basic_info/create", methods=["GET", "POST"])
def create_basic_info():
    form = BasicInfoForm()
    if form.validate_on_submit():
        print("Form submitted for validation")
        try:
            entry_title = form.entry_title.data
            full_name = form.full_name.data
            job_title = form.job_title.data
            address = form.address.data
            contact_email = form.contact_email.data
            contact_phone = form.contact_phone.data
            linkedin_url = form.linkedin_url.data
            github_url = form.github_url.data
            new_basic_info = BasicInfo(
                entry_title=entry_title,
                full_name=full_name,
                job_title=job_title,
                address=address,
                contact_email=contact_email,
                contact_phone=contact_phone,
                linkedin_url=linkedin_url,
                github_url=github_url,
                user_id=current_user.id,
            )
            db.session.add(new_basic_info)
            db.session.commit()
            flash("New Basic Info Created!", "success")
            return redirect(url_for("resume.list_basic_info"))
        except Exception as e:
            flash(f"Error while saving Basic Info: {e}")
            return redirect(url_for("resume.create_basic_info"))

    return render_template("resume_core/basic_info/create_basic_info.html", form=form)

#######################
## BASIC INFO: EDIT  ##
#######################

@login_required
@resume_bp.route("/basic_info/<string:info_id>/edit", methods=["GET", "POST"])
def edit_basic_info(info_id):
    """
    Handles editing an existing BasicInfo entry.
    """
    try:
        info_id_uuid = uuid.UUID(info_id)
    except ValueError:
        raise NotFound()

    info_to_edit = BasicInfo.query.filter_by(
        id=info_id, user_id=current_user.id
    ).first()
    if not info_to_edit:
        raise NotFound()

    form = BasicInfoForm(obj=info_to_edit)

    if form.validate_on_submit():
        try:
            # Update the object's attributes from the submitted form data
            form.populate_obj(info_to_edit)
            db.session.commit()
            flash("Your 'Basic Info' section has been updated!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating basic info entry: {e}", "danger")
        finally:
            return redirect(url_for("resume.list_basic_info"))

    # For a GET request, render the template with the pre-filled form
    return render_template(
        "resume_core/basic_info/edit_basic_info.html", form=form, info_id=info_id
    )

########################
## BASIC INFO: DELETE ##
########################

@login_required
@resume_bp.route("/basic_info/<string:info_id>/delete", methods=["GET"])
def delete_basic_info(info_id):
    """
    Handles deleting an existing BasicInfo entry.
    """
    try:
        info_to_delete = BasicInfo.query.filter_by(
            id=info_id, user_id=current_user.id
        ).first()
        if not info_to_delete:
            raise NotFound()
        db.session.delete(info_to_delete)
        db.session.commit()
        flash("Successfully deleted Basic Info entry.", "danger")
    except Exception as e:
        flash(f"Error while deleting Basic Info entry: {e}", "danger")

    return redirect(url_for("resume.list_basic_info"))



#######################
######  SUMMARY  ######
#######################

#########################
## SUMMARY: LIST VIEW  ##
#########################

@login_required
@resume_bp.route("/summary_list", methods=["GET", "POST"])
def list_summary():
    summaries = Summary.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/summary/list_summary.html", summaries=summaries)


#####################
## SUMMARY: CREATE ##
#####################

@login_required
@resume_bp.route("/summary/create", methods=["GET", "POST"])
def create_summary():
    form = SummaryForm()
    if form.validate_on_submit():
        try:
            entry_title = form.entry_title.data
            content = form.content.data
            new_summary = Summary(entry_title=entry_title, content=content, user_id=current_user.id)
            db.session.add(new_summary)
            db.session.commit()
            flash("New Summary created.", "success")
        except Exception as e:
            flash(f"Error while creating Summary: {e}", "danger")
        finally:
            return redirect(url_for('resume.list_summary'))   
    
    return render_template("resume_core/summary/create_summary.html", form=form)


####################
## SUMMARY: EDIT  ##
####################

@login_required
@resume_bp.route("/summary/<string:summary_id>/edit", methods=["GET", "POST"])
def edit_summary(summary_id):
    """
    Handles editing an existing BasicInfo entry.
    """
    try:
        summary_id_uuid = uuid.UUID(summary_id)
    except ValueError:
        raise NotFound()

    summary_to_edit = Summary.query.filter_by(
        id=summary_id_uuid, user_id=current_user.id
    ).first()
    if not summary_to_edit:
        raise NotFound()

    form = SummaryForm(obj=summary_to_edit)

    if form.validate_on_submit():
        try:
            form.populate_obj(summary_to_edit)
            db.session.commit()
            flash("Summary updated.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating summary: {e}", "danger")
        finally:
            return redirect(url_for("resume.list_summary"))

    return render_template(
        "resume_core/summary/edit_summary.html", form=form, summary_id=summary_id 
    )

#####################
## SUMMARY: DELETE ##
#####################

@login_required
@resume_bp.route("/summary/<string:summary_id>/delete", methods=["GET", "POST"])
def delete_summary(summary_id):
    try:
        summary_to_delete = Summary.query.filter_by(
            id=summary_id, user_id=current_user.id
        ).first()
        if not summary_to_delete:
            raise NotFound()
        db.session.delete(summary_to_delete)
        db.session.commit()
        flash("Summary deleted successfully.", "success")
    except Exception as e:
        flash(f"Error while deleting summary: {e}", "danger")

    return redirect(url_for("resume.list_summary"))



#########################
######  EXPERIENCE ######
#########################

###########################
## EXPERIENCE: LIST VIEW ##
###########################

@login_required
@resume_bp.route("/experience_list", methods=["GET", "POST"])
def list_experience():
    experiences = Experience.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/experience/list_experience.html", experiences=experiences)


########################
## EXPERIENCE: CREATE ##
########################

@login_required
@resume_bp.route("/experience/create", methods=["GET", "POST"])
def create_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        print("Form submitted for validation")
        try:
            new_experience = Experience()
            form.populate_obj(new_experience)
            new_experience.user_id = current_user.id
            db.session.add(new_experience)
            db.session.commit()
            flash("New Experience created.", "success")
            return redirect(url_for("resume.list_experience"))
        except Exception as e:
            flash(f"Error while creating Experience: {e}")
            return redirect(url_for("resume.create_experience"))

    return render_template("resume_core/experience/create_experience.html", form=form)


########################
## EXPERIENCE: EDIT   ##
########################

@login_required
@resume_bp.route("/experience/<string:experience_id>/edit", methods=["GET", "POST"])
def edit_experience(experience_id):
    """
    Handles editing an existing Experience entry.
    """
    try:
        experience_id_uuid = uuid.UUID(experience_id)
    except ValueError:
        raise NotFound()

    # Query for the specific BasicInfo object or raise a 404 error.
    # The filter also ensures a user can only edit their own entries.
    experience_to_edit = Experience.query.filter_by(
        id=experience_id_uuid, user_id=current_user.id
    ).first()
    if not experience_to_edit:
        raise NotFound()

    form = ExperienceForm(obj=experience_to_edit)

    if form.validate_on_submit():
        try:
            form.populate_obj(experience_to_edit)
            db.session.commit()
            flash("Experience updated.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating experience: {e}", "danger")
        finally:
            return redirect(url_for("resume.list_experience"))

    # For a GET request, render the template with the pre-filled form
    return render_template(
        "resume_core/experience/edit_experience.html", form=form, experience_id=experience_id
    )


########################
## EXPERIENCE: DELETE ##
########################

@login_required
@resume_bp.route("/experience/<string:experience_id>/delete")
def delete_experience(experience_id):
    try:
        exp_to_delete = Experience.query.filter_by(id=experience_id, user_id=current_user.id).first()
        if not exp_to_delete:
            return NotFound()
        db.session.delete(exp_to_delete)
        db.session.commit()
        flash("Successfully deleted work experience entry.", "success")
        return redirect(url_for("resume.list_experience"))
    except Exception as e:
        flash(f"Error while deleting experience: {e}", "danger")
        return redirect(url_for("resume.list_experience"))
    


###############
## EDUCATION ##
###############

@login_required
@resume_bp.route("/education_list", methods=["GET", "POST"])
def list_education():
    return "<h3>Education page</h3>"

############
## SKILLS ##
############

@login_required
@resume_bp.route("/skills", methods=["GET", "POST"])
def skills():
    return "<h3>Skills page</h3>"


###############
## LANGUAGES ##
###############

@login_required
@resume_bp.route("/languages", methods=["GET", "POST"])
def languages():
    return "<h3>Languages page</h3>"
