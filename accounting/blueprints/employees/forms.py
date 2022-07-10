from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EmployeesForm(FlaskForm):
    employee_name = StringField(label="Employee Name", validators=[DataRequired()])
    employee_tin = StringField(label="TIN")
    submit = SubmitField(label="Save")
