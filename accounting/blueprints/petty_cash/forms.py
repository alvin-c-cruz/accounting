from flask_wtf import FlaskForm, Form
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired, optional


class PettyCashEntryForm(Form):
    entry_id = HiddenField(label="id")
    petty_cash_id = StringField(label="Petty Cash ID")
    account_id = SelectField(label="Account Title")
    debit = StringField(label="Debit", default="0.00")
    credit = StringField(label="Credit", default="0.00")
    notes = StringField(label="Notes")


class PettyCashForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    report_date = DateField(label="Report Date", validators=[optional()])
    petty_cash_number = StringField(label="PCF Number", validators=[DataRequired()])
    invoice_number = StringField(label="Invoice Number")
    notes = TextAreaField(label="Description")
    vendor_id = SelectField(label="Vendor", validators=[DataRequired()])

    entries = FieldList(FormField(PettyCashEntryForm), min_entries=10)

    submit = SubmitField(label="Save")


class JournalDateRange(FlaskForm):
    date_from = DateField(label="From", validators=[DataRequired()])
    date_to = DateField(label="To", validators=[DataRequired()])

    submit = SubmitField(label="Download Journal")
