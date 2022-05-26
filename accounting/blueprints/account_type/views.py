from flask import Blueprint, render_template, redirect, url_for, flash
from .models import AccountType
from .forms import AccountTypeForm

bp = Blueprint("account_type", __name__, template_folder="pages", url_prefix="/account_type")


@bp.route("/")
def home():
    account_types = AccountType.query.order_by(AccountType.priority).all()
    return render_template("account_type/home.html", account_types=account_types)


@bp.route("/add", methods=["GET", "POST"])
def add():
    form = AccountTypeForm()
    if form.validate_on_submit():
        new_data = AccountType()
        new_data.data(form)
        new_data.save_and_commit()
        flash(f"Added {new_data}", category="success")
        return redirect(url_for("account_type.home"))
    return render_template("account_type/add.html", form=form)


@bp.route("/edit/<id>")
def edit(id):
    return "Edit record."


@bp.route("/delete/<id>")
def delete(id):
    return "Delete record."

