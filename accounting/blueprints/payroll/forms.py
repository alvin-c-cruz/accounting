from flask_wtf import FlaskForm, Form
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired


class PayrollEntryForm(Form):
    entry_id = HiddenField(label="id")
    payroll_id = StringField(label="Payroll ID")
    account_id = SelectField(label="Account Title")
    debit = StringField(label="Debit", default="0.00")
    credit = StringField(label="Credit", default="0.00")
    notes = StringField(label="Notes")


class PayrollForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    payroll_number = StringField(label="Payroll Number", validators=[DataRequired()])
    notes = TextAreaField(label="Description")
    employee_id = SelectField(label="Employee", validators=[DataRequired()])

    entries = FieldList(FormField(PayrollEntryForm), min_entries=10)

    submit = SubmitField(label="Save")


class JournalDateRange(FlaskForm):
    date_from = DateField(label="From", validators=[DataRequired()])
    date_to = DateField(label="To", validators=[DataRequired()])

    submit = SubmitField(label="Download Journal")
