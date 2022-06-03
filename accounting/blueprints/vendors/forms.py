from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class VendorsForm(FlaskForm):
    vendor_name = StringField(label="Vendor Name", validators=[DataRequired()])
    vendor_tin = StringField(label="TIN")
    submit = SubmitField(label="Save")