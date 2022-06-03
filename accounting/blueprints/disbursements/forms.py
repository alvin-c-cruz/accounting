from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class DisbursementsForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    bank_date = DateField(label="Bank Date")
    disbursement_number = StringField(label="CD Number", validators=[DataRequired()])
    check_number = StringField(label="Check Number", validators=[DataRequired()])
    notes = TextAreaField(label="Description")
    vendor_id = SelectField(label="Vendor", validators=[DataRequired()])

    submit = SubmitField(label="Save")