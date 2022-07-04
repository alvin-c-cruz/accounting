from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from accounting import db
from .forms import UserForm, LoginForm
from .models import User
from .token import generate_confirmation_token, confirm_token
from .email import send_email

bp = Blueprint('user', __name__, template_folder="pages", url_prefix="/user")


@bp.route("/")
@login_required
def home():
    return render_template("user/home.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if User.query.filter_by(email=email).first():
            flash(message="Email already registered.", category="error")
        elif password != confirm_password:
            flash(message="Password does not match.", category="error")
        else:
            user = User(
                email=email,
                name=name,
                password=generate_password_hash(password),
                registered_on=datetime.now()
            )
            db.session.add(user)
            db.session.commit()

            # send_confirmation_email(email)

            login_user(user)

            flash(message="Registration successful. Please confirmation message has been sent to your email.",
                  category="success")

            return redirect(url_for('landing_page.home'))
    return render_template("user/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Login in successful.", "success")
                return redirect(url_for('landing_page.home'))

        flash("Name or password is incorrect.", "error")
    return render_template("user/login.html", form=form)


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing_page.home'))


@bp.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = confirm_token(app=current_app, token=token)
    except:
        flash("The confirmation link is invalid or has expired.", 'error')
        return redirect(url_for("landing_page.home"))

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed_on:
        flash("Account already confirmed.", "success")
    else:
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("You have confirmed your account. Thank you.", "success")
    return redirect(url_for("landing_page.home"))


def send_confirmation_email(email):
    token = generate_confirmation_token(app=current_app, email=email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_app, to=email, subject=subject, html=html)
