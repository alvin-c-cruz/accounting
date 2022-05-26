from flask import Blueprint, redirect, url_for, flash
from flask_login import login_user
from datetime import datetime

bp = Blueprint('transition', __name__, url_prefix="/transition")


@bp.route("/")
def home():
    default_user()
    flash("Data reloaded.", category="success")
    return redirect(url_for("landing_page.home"))


def default_user():
    name = "Alvin"
    email = "alvinccruz12@gmail.com"
    password = "pbkdf2:sha256:260000$SUwzS5Td2dcLQQUY$c88f053d0e5fdacd8f25795d0b3d51f9297059c7556335b3951ba87191884625"
    registered_on = confirmed_on = datetime.now()

    from .. user import User

    User.query.delete()
    new_user = User(
        name=name,
        email=email,
        password=password,
        admin=True,
        registered_on=registered_on,
        confirmed_on=confirmed_on
    )
    new_user.save_and_commit()

    login_user(new_user)