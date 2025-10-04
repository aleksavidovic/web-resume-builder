import uuid

from weasyprint import HTML
from resume_builder.resume_builder_core.forms import (
    BasicInfoForm,
    EducationForm,
    ExperienceForm,
    SkillsForm,
    SummaryForm,
    LanguageForm,
    BuildResumeForm
)
from . import resume_bp
from flask import flash, redirect, render_template, url_for, Response, request
from flask_login import login_required, current_user
from ..models import BasicInfo, BuiltResume, Education, Language, ResumeTheme, Summary, Experience, Skills
from .. import db
from werkzeug.exceptions import NotFound


@login_required
@resume_bp.route("/", methods=["GET", "POST"])
def home():
    basic_info = BasicInfo.query.filter_by(user_id=current_user.id).all()
    summaries = Summary.query.filter_by(user_id=current_user.id).all()
    experiences = Experience.query.filter_by(user_id=current_user.id).all()
    educations = Education.query.filter_by(user_id=current_user.id).all()
    skills = Skills.query.filter_by(user_id=current_user.id).all()
    languages = Language.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "resume_core/home.html",
        basic_info=basic_info,
        summaries=summaries,
        experiences=experiences,
        educations=educations,
        skills=skills,
        languages=languages
    )


##########################
######  BASIC INFO  ######
##########################

###########################
## BASIC_INFO: LIST VIEW ##
###########################


@login_required
@resume_bp.route("/basic_info_list", methods=["GET", "POST"])
def list_basic_info():
    users_basic_info = BasicInfo.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "resume_core/basic_info/list_basic_info.html", basic_infos=users_basic_info
    )


########################
## BASIC_INFO: CREATE ##
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
## BASIC_INFO: EDIT  ##
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
## BASIC_INFO: DELETE ##
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
            new_summary = Summary(
                entry_title=entry_title, content=content, user_id=current_user.id
            )
            db.session.add(new_summary)
            db.session.commit()
            flash("New Summary created.", "success")
        except Exception as e:
            flash(f"Error while creating Summary: {e}", "danger")
        finally:
            return redirect(url_for("resume.list_summary"))

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
    return render_template(
        "resume_core/experience/list_experience.html", experiences=experiences
    )


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
            from resume_builder.resume_builder_core.html_utils import render_markdown
            new_experience = Experience()
            form.populate_obj(new_experience)
            new_experience.description = render_markdown(form.description.data)
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
        "resume_core/experience/edit_experience.html",
        form=form,
        experience_id=experience_id,
    )


########################
## EXPERIENCE: DELETE ##
########################


@login_required
@resume_bp.route("/experience/<string:experience_id>/delete")
def delete_experience(experience_id):
    try:
        exp_to_delete = Experience.query.filter_by(
            id=experience_id, user_id=current_user.id
        ).first()
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
##########################
## EDUCATION: LIST VIEW ##
##########################


@login_required
@resume_bp.route("/education_list", methods=["GET", "POST"])
def list_education():
    educations = Education.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "resume_core/education/list_education.html", educations=educations
    )


#######################
## EDUCATION: CREATE ##
#######################


@login_required
@resume_bp.route("/create_education", methods=["GET", "POST"])
def create_education():
    form = EducationForm()
    if form.validate_on_submit():
        new_education = Education()
        form.populate_obj(new_education)
        new_education.user_id = current_user.id
        db.session.add(new_education)
        db.session.commit()
        flash("New education created.", "success")
        return redirect(url_for("resume.list_education"))
    return render_template("resume_core/education/create_education.html", form=form)


#####################
## EDUCATION: EDIT ##
#####################


@login_required
@resume_bp.route("/education/<string:education_id>/edit", methods=["GET", "POST"])
def edit_education(education_id):
    education_to_edit = Education.query.filter_by(
        id=education_id, user_id=current_user.id
    ).first()
    if not education_to_edit:
        return NotFound()
    form = EducationForm(obj=education_to_edit)
    if form.validate_on_submit():
        try:
            form.populate_obj(education_to_edit)
            db.session.commit()
            flash("Education edited successfully", "success")
        except Exception as e:
            flash(f"Error while editing education: {e}", "danger")
        finally:
            return redirect(url_for("resume.list_education"))
    return render_template(
        "resume_core/education/edit_education.html",
        form=form,
        education_id=education_id,
    )


#######################
## EDUCATION: DELETE ##
#######################


@login_required
@resume_bp.route("/education/<string:education_id>/delete")
def delete_education(education_id):
    try:
        education_to_delete = Education.query.filter_by(
            id=education_id, user_id=current_user.id
        ).first()
        if not education_to_delete:
            return NotFound()
        db.session.delete(education_to_delete)
        db.session.commit()
        flash("Education deleted.", "success")
    except Exception as e:
        flash(f"Error deleting education: {e}", "danger")
    finally:
        return redirect(url_for("resume.list_education"))


############
## SKILLS ##
############
##################
## SKILLS: LIST ##
##################


@login_required
@resume_bp.route("/skills_list", methods=["GET", "POST"])
def list_skills():
    skills = Skills.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/skills/list_skills.html", skills=skills)


####################
## SKILLS: CREATE ##
####################


@login_required
@resume_bp.route("/create_skills", methods=["GET", "POST"])
def create_skills():
    form = SkillsForm()
    if form.validate_on_submit():
        new_skills = Skills()
        form.populate_obj(new_skills)
        new_skills.user_id = current_user.id
        db.session.add(new_skills)
        db.session.commit()
        flash("New skills added", "success")
        return redirect(url_for('resume.list_skills'))
    return render_template("resume_core/skills/create_skills.html", form=form)

##################
## SKILLS: EDIT ##
##################


@login_required
@resume_bp.route("/skills/<string:skill_id>/edit", methods=["GET", "POST"])
def edit_skill(skill_id):
    skill_to_edit = Skills.query.filter_by(id=skill_id, user_id=current_user.id).first_or_404()
    form = SkillsForm()
    if form.validate_on_submit():
        form.populate_obj(skill_to_edit)
        db.session.commit()
        flash("Skill updated.", "success")
        return redirect(url_for("resume.list_skills"))
    form = SkillsForm(obj=skill_to_edit)
    return render_template("resume_core/skills/edit_skill.html", form=form, skill_id=skill_id)

####################
## SKILLS: DELETE ##
####################


@login_required
@resume_bp.route("/skills/<string:skills_id>/delete")
def delete_skills(skills_id):
    skills_to_delete = Skills.query.filter_by(id=skills_id, user_id=current_user.id).first()
    if not skills_to_delete:
        return NotFound()
    db.session.delete(skills_to_delete)
    db.session.commit()
    flash("Skills deleted successfully", "success")
    return redirect(url_for('resume.list_skills'))
    

###############
## LANGUAGES ##
###############
#####################
## LANGUAGES: LIST ##
#####################

@login_required
@resume_bp.route("/languages_list", methods=["GET"])
def list_languages():
    languages = Language.query.filter_by(user_id=current_user.id)
    return render_template('resume_core/languages/list_languages.html', languages=languages)


#######################
## LANGUAGES: CREATE ##
#######################

@login_required
@resume_bp.route("/create_language", methods=["GET", "POST"])
def create_language():
    form = LanguageForm()
    if form.validate_on_submit():
        try:
            new_language = Language()
            form.populate_obj(new_language)
            new_language.user_id = current_user.id
            db.session.add(new_language)
            db.session.commit()
            flash("New language added.", "success")
        except Exception as e:
            flash(f"Error adding new language: {e}", "danger")
        finally:
            return redirect(url_for('resume.list_languages'))
    return render_template("resume_core/languages/create_language.html", form=form)


#####################
## LANGUAGES: EDIT ##
#####################


@login_required
@resume_bp.route("/languages/<string:language_id>/edit", methods=["GET", "POST"])
def edit_language(language_id):
    language_to_edit = Language.query.filter_by(id=language_id, user_id=current_user.id).first()
    if not language_to_edit:
        return NotFound()
    form = LanguageForm(obj=language_to_edit)
    if form.validate_on_submit():
        try:
            form.populate_obj(language_to_edit)
            db.session.commit()
            flash("Language updated.", "success")
        except Exception as e:
            flash(f"Error while updating language: {e}.", "danger")
        finally:
            return redirect(url_for('resume.list_languages'))
    return render_template("resume_core/languages/edit_language.html", form=form, language_id=language_id)


#######################
## LANGUAGES: DELETE ##
#########@#############


@login_required
@resume_bp.route("/languages/<string:language_id>/delete")
def delete_language(language_id):
    language_to_delete = Language.query.filter_by(id=language_id, user_id=current_user.id).first()
    if not language_to_delete:
        return NotFound()
    db.session.delete(language_to_delete)
    db.session.commit()
    flash("Language deleted successfully", "success")
    return redirect(url_for('resume.list_languages'))
    



##################
## RESUME BUILD ##
##################
#############################
## RESUME BUILD: LIST VIEW ##
#############################


@login_required
@resume_bp.route("/list_resume", methods=["GET", "POST"])
def list_resume():
    resumes = BuiltResume.query.filter_by(user_id=current_user.id).all()
    return render_template("resume_core/build_resume/list_resume.html", resumes=resumes)


#################################
## RESUME BUILD: CREATE RESUME ##
#################################

@login_required
@resume_bp.route("/build_resume", methods=["GET", "POST"])
def build_resume():
    form = BuildResumeForm()
    themes = ResumeTheme.query.all()
    
    form.basic_info.choices = [(info.id, info.entry_title) for info in current_user.basic_infos]
    form.summary.choices = [(summary.id, summary.entry_title) for summary in current_user.summaries]
    form.experience.choices = [(exp.id, exp.entry_title) for exp in current_user.experiences]
    form.education.choices = [(edu.id, edu.entry_title) for edu in current_user.education]
    form.skills.choices = [(skill.id, skill.entry_title) for skill in current_user.skills]
    form.languages.choices = [(lang.id, lang.entry_title) for lang in current_user.languages]
    form.theme.choices = [(theme.id, theme.name) for theme in themes]
    
    if form.validate_on_submit():
        new_resume = BuiltResume(
            entry_title=form.entry_title.data,
            basic_info_id=form.basic_info.data,
            summary_id=form.summary.data,
            user_id=current_user.id,
            theme_id=form.theme.data,
        )

        # Populate many-to-many relationshiop tables
        new_resume.experience = Experience.query.filter(
            Experience.id.in_(form.experience.data)
        ).all()
        new_resume.education = Education.query.filter(
            Education.id.in_(form.education.data)
        ).all()
        new_resume.skills= Skills.query.filter(
            Skills.id.in_(form.skills.data)
        ).all()
        new_resume.languages = Language.query.filter(
            Language.id.in_(form.languages.data)
        ).all()
        

        db.session.add(new_resume)
        db.session.commit()

        flash("Resume created.", "success")
        return redirect(url_for("resume.list_resume"))

    return render_template("resume_core/build_resume/build_resume.html", 
                           form=form)


###############################
## RESUME BUILD: EDIT RESUME ##
###############################


@login_required
@resume_bp.route("/resumes/<string:resume_id>/edit", methods=["GET", "POST"])
def edit_resume(resume_id):
    resume_to_edit = BuiltResume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    form = BuildResumeForm()
    themes = ResumeTheme.query.all()

    # --- Populate choices using STRINGS for the IDs ---
    form.basic_info.choices = [(str(info.id), info.entry_title) for info in current_user.basic_infos]
    form.summary.choices = [(str(summary.id), summary.entry_title) for summary in current_user.summaries]
    form.experience.choices = [(str(exp.id), exp.entry_title) for exp in current_user.experiences]
    form.education.choices = [(str(edu.id), edu.entry_title) for edu in current_user.education]
    form.skills.choices = [(str(skill.id), skill.entry_title) for skill in current_user.skills]
    form.languages.choices = [(str(lang.id), lang.entry_title) for lang in current_user.languages]
    form.theme.choices = [(str(theme.id), theme.name) for theme in themes]

    if form.validate_on_submit():
        # --- Handle POST Request (This part remains largely the same) ---
        try:
            resume_to_edit.entry_title = form.entry_title.data
            resume_to_edit.basic_info_id = form.basic_info.data
            resume_to_edit.summary_id = form.summary.data
            resume_to_edit.theme_id = form.theme.data
            
            resume_to_edit.experience = Experience.query.filter(Experience.id.in_(form.experience.data)).all()
            resume_to_edit.education = Education.query.filter(Education.id.in_(form.education.data)).all()
            resume_to_edit.skills = Skills.query.filter(Skills.id.in_(form.skills.data)).all()
            resume_to_edit.languages = Language.query.filter(Language.id.in_(form.languages.data)).all()

            db.session.commit()
            flash("Resume updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error while updating resume: {e}", "danger")
        finally:
            return redirect(url_for("resume.list_resume"))
    
    # --- Handle GET Request (Populating the form for editing using STRINGS) ---
    if request.method == 'GET':
        form.entry_title.data = resume_to_edit.entry_title
        form.basic_info.data = str(resume_to_edit.basic_info_id)
        form.summary.data = str(resume_to_edit.summary_id)
        form.theme.data = str(resume_to_edit.theme_id)
        
        # For multi-value fields, set data to a list of STRING IDs
        form.experience.data = [str(exp.id) for exp in resume_to_edit.experience]
        form.education.data = [str(edu.id) for edu in resume_to_edit.education]
        form.skills.data = [str(skill.id) for skill in resume_to_edit.skills]
        form.languages.data = [str(lang.id) for lang in resume_to_edit.languages]

    return render_template("resume_core/build_resume/edit_resume.html", form=form, resume_id=resume_id)

####################
## RESUME: DELETE ##
####################


@login_required
@resume_bp.route("/resumes/<string:resume_id>/delete", methods=["GET", "POST"])
def delete_resume(resume_id):
    try:
        resume_to_delete = BuiltResume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
        db.session.delete(resume_to_delete)
        db.session.commit()
        flash('Resume removed.', 'success')
    except Exception as e:
        flash(f'Error while removing Resume: {e}.', 'danger')
    finally:
        return redirect(url_for('resume.list_resume'))



#####################
## RESUME: PREVIEW ##
#####################

@login_required
@resume_bp.route("resumes/<string:resume_id>/preview", methods=["GET"])
def preview_resume(resume_id):
    resume_to_preview = BuiltResume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    return render_template("resume_core/build_resume/preview_resume.html", resume=resume_to_preview) 


#####################################
## RESUME: GENERATE & DOWNLOAD PDF ##
#####################################


@login_required
@resume_bp.route("/resume/<string:resume_id>/download", methods=["GET"])
def download_resume(resume_id):
    resume_to_generate = BuiltResume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    html = render_template("resume_core/build_resume/resume_pdf.html", resume=resume_to_generate, theme=resume_to_generate.theme)
    pdf = HTML(string=html).write_pdf()
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f"attachment;filename={resume_to_generate.entry_title.replace(' ', '_')}"
        }
    )
