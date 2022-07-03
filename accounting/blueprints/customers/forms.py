from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CustomerForm(FlaskForm):
    customer_name = StringField(label="Customer Name", validators=[DataRequired()])
    customer_tin = StringField(label="TIN")
    submit = SubmitField(label="Save")
