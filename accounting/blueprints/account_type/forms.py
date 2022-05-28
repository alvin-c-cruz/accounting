from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from .models import AccountType


class AccountTypeForm(FlaskForm):
    account_type = StringField(label="Description", validators=[DataRequired()])
    classification = SelectField(
        label="Classification",
        validators=[DataRequired()],
        choices=AccountType.classification_choices()
    )
    prefix = StringField(label="Prefix", validators=[DataRequired()])
    submit = SubmitField(label="Save")