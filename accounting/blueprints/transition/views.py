from flask import Blueprint, redirect, url_for, flash, current_app
from flask_login import login_user
from datetime import datetime
import os
import json

from .. account_type import AccountType
from .. vendors import Vendors

from .. accounts import Accounts

bp = Blueprint('transition', __name__, url_prefix="/transition")


@bp.route("/")
def home():
    default_user()
    reload(AccountType)
    reload(Vendors)

    reload(Accounts)
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


def reload(obj):
    obj().delete_all()

    with current_app.app_context():
        filename = os.path.join(current_app.instance_path, "uploads", f"{obj.__tablename__}.json")

    with open(filename, "r") as f:
        json_data = json.load(f)

    for row in json_data:
        new_data = obj()
        for key, value in row.items():
            if key != "id":
                setattr(new_data, key, value)
        new_data.save_and_commit()
