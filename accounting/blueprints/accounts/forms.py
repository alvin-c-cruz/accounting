from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from .. data_model import DataModel
from .. account_type import AccountType


class AccountsForm(FlaskForm, DataModel):
    account_number = StringField(label="Account Number", validators=[DataRequired()])
    account_title = StringField(label="Account Title", validators=[DataRequired()])
    account_type_id = SelectField(label="Account Type", validators=[DataRequired()])
    submit = SubmitField(label="Save")