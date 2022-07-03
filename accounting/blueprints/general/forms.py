from flask_wtf import FlaskForm, Form
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired, optional


class GeneralEntryForm(Form):
    entry_id = HiddenField(label="id")
    general_id = StringField(label="General ID")
    account_id = SelectField(label="Account Title")
    debit = StringField(label="Debit", default="0.00")
    credit = StringField(label="Credit", default="0.00")
    notes = StringField(label="Notes")


class GeneralForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    general_number = StringField(label="General Voucher Number", validators=[DataRequired()])
    notes = TextAreaField(label="Description")

    entries = FieldList(FormField(GeneralEntryForm), min_entries=10)

    submit = SubmitField(label="Save")


class JournalDateRange(FlaskForm):
    date_from = DateField(label="From", validators=[DataRequired()])
    date_to = DateField(label="To", validators=[DataRequired()])

    submit = SubmitField(label="Download Journal")
