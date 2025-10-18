from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ThemeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    description = StringField("Descritpion", validators=[Length(max=200)])
    styles = TextAreaField("Stylesheet code", validators=[DataRequired()])
    submit = SubmitField("Create Theme")


class CreateInviteCodeForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    description = StringField("Descritpion", validators=[Length(max=200)])
    submit = SubmitField("Create Code")
