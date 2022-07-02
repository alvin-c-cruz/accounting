from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CompanyForm(FlaskForm):
    company_name = StringField(label="Company Name", validators=[DataRequired()])

    disbursement_prepared = StringField(label="Prepared by")
    disbursement_check = StringField(label="Checked by")
    disbursement_audited = StringField(label="Audited by")
    disbursement_approved = StringField(label="Approved by")

    submit = SubmitField(label="Save")
