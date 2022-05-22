from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()],
                       render_kw={"autocomplete": "off", "placeholder": "Type your name here"})
    email = EmailField(label="Email", validators=[DataRequired(), Email()],
                       render_kw={"autocomplete": "off", "placeholder": "Type your email here"})
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)],
                             render_kw={"placeholder": "Password must 8 characters or more"})
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), Length(min=8)],
                                     render_kw={"placeholder": "Re-type password"})

    submit = SubmitField(label="Register", render_kw={"class_": "btn btn-success"})


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email()], render_kw={"autocomplete": "off"})
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In", render_kw={"class_": "btn btn-success"})
