from flask_wtf import FlaskForm, Form
from wtforms import (
    StringField,
    DateField,
    TextAreaField,
    SelectField,
    SubmitField,
    FormField,
    FieldList,
    HiddenField,
    FloatField
)
from wtforms.validators import DataRequired, optional


class AccountsPayableEntryForm(Form):
    entry_id = HiddenField(label="id")
    accounts_payable_id = StringField(label="Payable ID")
    account_id = SelectField(label="Account Title")
    debit = FloatField(label="Debit", default=0)
    credit = FloatField(label="Credit", default=0)
    notes = StringField(label="Notes")


class AccountsPayableForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    due_date = DateField(label="Due Date", validators=[optional()])
    accounts_payable_number = StringField(label="AP Number", validators=[DataRequired()])
    invoice_number = StringField(label="Invoice Number")
    notes = TextAreaField(label="Description")
    vendor_id = SelectField(label="Vendor", validators=[DataRequired()])

    entries = FieldList(FormField(AccountsPayableEntryForm), min_entries=10)

    submit = SubmitField(label="Save")


class JournalDateRange(FlaskForm):
    date_from = DateField(label="From", validators=[DataRequired()])
    date_to = DateField(label="To", validators=[DataRequired()])

    submit = SubmitField(label="Download Journal")
