import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, send_file, current_app
from flask_login import login_required
from .models import AccountType
from .forms import AccountTypeForm

bp = Blueprint("account_type", __name__, template_folder="pages", url_prefix="/account_type")


@bp.route("/<int:page>")
@login_required
def home(page):
    account_types = AccountType.query.order_by(AccountType.prefix).paginate(page=page, per_page=10)
    return render_template("account_type/home.html", account_types=account_types)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AccountTypeForm()
    if form.validate_on_submit():
        new_data = AccountType()
        new_data.data(form)
        new_data.save_and_commit()
        flash(f"Added {new_data}", category="success")
        return redirect(url_for("account_type.home", page=1))
    return render_template("account_type/add.html", form=form)


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = AccountType.query.get(id)
    form = AccountTypeForm(obj=data_to_edit)
    if form.validate_on_submit():
        data_to_edit.data(form)
        data_to_edit.save_and_commit()
        flash(f"Edited {data_to_edit}", category="success")
        return redirect(url_for("account_type.home", page=1))
    return render_template("account_type/edit.html", form=form, id=id)


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    data_to_delete = AccountType.query.get(id)
    data_to_delete.delete_and_commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for("account_type.home", page=1))


@bp.route("/export")
@login_required
def export():
    filename = AccountType().export()

    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)

