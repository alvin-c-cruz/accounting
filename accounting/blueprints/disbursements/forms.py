from flask_wtf import FlaskForm, Form
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FormField, FieldList, HiddenField, DecimalRangeField
from wtforms.validators import DataRequired, optional
from datetime import datetime


class DisbursementsEntryForm(Form):
    entry_id = HiddenField(label="id")
    disbursement_id = StringField(label="Disbursement ID")
    account_id = SelectField(label="Account Title")
    debit = StringField(label="Debit", default="0.00")
    credit = StringField(label="Credit", default="0.00")
    notes = StringField(label="Notes")


class DisbursementsForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    bank_date = DateField(label="Bank Date", validators=[optional()])
    disbursement_number = StringField(label="CD Number", validators=[DataRequired()])
    check_number = StringField(label="Check Number", validators=[DataRequired()])
    notes = TextAreaField(label="Description")
    vendor_id = SelectField(label="Vendor", validators=[DataRequired()])

    entries = FieldList(FormField(DisbursementsEntryForm), min_entries=5)

    submit = SubmitField(label="Save")


class JournalDateRange(FlaskForm):
    date_from = DateField(label="From")
    date_to = DateField(label="To")

    submit = SubmitField(label="Download Journal")
