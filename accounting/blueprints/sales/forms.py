from flask_wtf import FlaskForm, Form
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired, optional


class SalesEntryForm(Form):
    entry_id = HiddenField(label="id")
    sales_id = StringField(label="Sales ID")
    account_id = SelectField(label="Account Title")
    debit = StringField(label="Debit", default="0.00")
    credit = StringField(label="Credit", default="0.00")
    notes = StringField(label="Notes")


class SalesForm(FlaskForm):
    record_date = DateField(label="Record Date", validators=[DataRequired()])
    bank_date = DateField(label="Bank Date", validators=[optional()])
    sales_number = StringField(label="Sales Number", validators=[DataRequired()])
    invoice_number = StringField(label="Invoice Number")
    notes = TextAreaField(label="Description")
    customer_id = SelectField(label="Customer", validators=[DataRequired()])

    entries = FieldList(FormField(SalesEntryForm), min_entries=10)

    submit = SubmitField(label="Save")


class JournalDateRange(FlaskForm):
    date_from = DateField(label="From", validators=[DataRequired()])
    date_to = DateField(label="To", validators=[DataRequired()])

    submit = SubmitField(label="Download Journal")
