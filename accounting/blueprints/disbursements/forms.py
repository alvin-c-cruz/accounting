from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired


class DisbursementsEntryForm(FlaskForm):
    account_id = SelectField(label="Account Title", validators=[DataRequired()])
    debit = StringField(label="Debit", default="0.00")
    credit = StringField(label="Debit", default="0.00")
    notes = StringField(label="Notes")


class DisbursementsForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    bank_date = DateField(label="Bank Date")
    disbursement_number = StringField(label="CD Number", validators=[DataRequired()])
    check_number = StringField(label="Check Number", validators=[DataRequired()])
    notes = TextAreaField(label="Description")
    vendor_id = SelectField(label="Vendor", validators=[DataRequired()])

    entries = FieldList(FormField(DisbursementsEntryForm), min_entries=10)

    submit = SubmitField(label="Save")


