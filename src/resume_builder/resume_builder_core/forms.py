from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, Length


class BasicInfoForm(FlaskForm):
    entry_title = StringField(
        "Entry Title", validators=[DataRequired(), Length(max=50)]
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
    content = TextAreaField("Summary Content", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Save Summary")
