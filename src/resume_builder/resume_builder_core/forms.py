from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Length, Optional

class MutiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class BasicInfoForm(FlaskForm):
    entry_title = StringField(
        "A name for your Basic Info entry", validators=[DataRequired(), Length(max=50)]
    )
    full_name = StringField(
        "Full Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    job_title = StringField("Job Title", validators=[DataRequired(), Length(max=50)])
    address = StringField("Address", validators=[DataRequired(), Length(max=50)])
    contact_email = StringField(
        "Contact Email", validators=[DataRequired(), Email(), Length(max=30)]
    )
    contact_phone = StringField(
        "Contact Phone", validators=[DataRequired(), Length(max=30)]
    )
    linkedin_url = StringField("Linkedin URL:", validators=[Length(max=100)])
    github_url = StringField("Github URL:", validators=[Length(max=100)])
    submit = SubmitField("Save Basic Info")


class SummaryForm(FlaskForm):
    entry_title = StringField(
        "Entry Title", validators=[DataRequired(), Length(max=50)]
    )
    content = TextAreaField(
        "Summary Content", validators=[DataRequired(), Length(max=500)]
    )
    submit = SubmitField("Save Summary")


class ExperienceForm(FlaskForm):
    entry_title = StringField(
        "Entry Title", validators=[DataRequired(), Length(max=50)]
    )
    job_title = StringField("Job Title", validators=[DataRequired(), Length(max=50)])
    company_name = StringField(
        "Company Name", validators=[DataRequired(), Length(max=50)]
    )
    date_started = DateField("Date Started", validators=[DataRequired()])
    date_finished = DateField("Date Finished", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Save Experience")


class EducationForm(FlaskForm):
    entry_title = StringField(
        "Entry Title", validators=[DataRequired(), Length(max=50)]
    )
    degree_name = StringField(
        "Degree Name", validators=[DataRequired(), Length(max=50)]
    )
    school_name = StringField(
        "School Name", validators=[DataRequired(), Length(max=50)]
    )
    date_started = DateField("Date Started", validators=[DataRequired()])
    date_finished = DateField("Date Finished", validators=[Optional()])
    submit = SubmitField("Save Education")
    

class SkillsForm(FlaskForm):
    entry_title = StringField(
        "Entry Title", validators=[DataRequired(), Length(max=50)]
    )
    description = TextAreaField(
        "Skill Description", validators=[DataRequired(), Length(max=500)]
    )
    submit = SubmitField("Save Skills")

class LanguageForm(FlaskForm):
    entry_title = StringField(
        "Entry Title", validators=[DataRequired(), Length(max=50)]
    )
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=30)]
    )
    proficiency = StringField(
        "Proficiency", validators=[DataRequired(), Length(max=30)]
    )
    submit = SubmitField("Save Skills")
    
class BuildResumeForm(FlaskForm):
    entry_title = StringField(
        "Entry Title", validators=[DataRequired(), Length(max=50)]
    )
    basic_info = SelectField("Basic Info", validators=[DataRequired()])
    summary = SelectField("Summary", validators=[DataRequired()])
    theme = SelectField("Theme", validators=[DataRequired()])
    experience = MutiCheckboxField("Experience", validators=[DataRequired()])
    education = MutiCheckboxField("Education", validators=[DataRequired()])
    skills = MutiCheckboxField("Skills", validators=[DataRequired()])
    languages = MutiCheckboxField("Languages", validators=[DataRequired()])

    
    submit = SubmitField("Generate Resume")
