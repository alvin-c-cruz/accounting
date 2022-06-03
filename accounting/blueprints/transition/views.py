from flask import Blueprint, redirect, url_for, flash, current_app
from flask_login import login_user
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import os
import json

from .. account_type import AccountType
from .. vendors import Vendors

from .. accounts import Accounts

bp = Blueprint('transition', __name__, url_prefix="/transition")


@bp.route("/")
def home():
    test_user()
    default_user()
    reload(AccountType)
    reload(Vendors)

    reload(Accounts)
    flash("Data reloaded.", category="success")
    return redirect(url_for("landing_page.home"))


def test_user():
    name = "test"
    email = "test@gmail.com"
    password = "ac112557"
    registered_on = confirmed_on = datetime.now()

    from ..user import User
    User.query.delete()

    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=16),
        admin=False,
        registered_on=registered_on,
        confirmed_on=confirmed_on
    )
    new_user.save_and_commit()


def default_user():
    name = "Alvin"
    email = "alvinccruz12@gmail.com"
    password = "ac112557"
    registered_on = confirmed_on = datetime.now()

    from .. user import User


    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=16),
        admin=True,
        registered_on=registered_on,
        confirmed_on=confirmed_on
    )
    new_user.save_and_commit()

    login_user(new_user)


def reload(obj):
    obj().delete_all()

    with current_app.app_context():
        filename = os.path.join(current_app.instance_path, "uploads", f"{obj.__tablename__}.json")

    try:
        with open(filename, "r") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = []

    for row in json_data:
        new_data = obj()
        for key, value in row.items():
            if key == "id":
                continue
            if 'date' in key:
                if value:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

            setattr(new_data, key, value)

        new_data.save_and_commit()
