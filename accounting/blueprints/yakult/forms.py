from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class YakultForm(FlaskForm):
    age_group = SelectField("Age Group", validators=[DataRequired()], choices=["", "Adult", "Child", "Infant"])
    submit = SubmitField("Submit")
