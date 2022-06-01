from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask_login import login_required
from .models import Accounts
from .forms import AccountsForm
from .. account_type import AccountType

bp = Blueprint('accounts', __name__, template_folder="pages", url_prefix="/accounts")


@bp.route("/<int:page>")
@login_required
def home(page):
    accounts = Accounts.query.order_by(Accounts.account_number).paginate(page=page, per_page=10)
    return render_template("accounts/home.html", accounts=accounts)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AccountsForm()
    form.account_type_id.choices = account_type_choices()

    if form.validate_on_submit():
        new_data = Accounts()
        new_data.data(form)
        new_data.save_and_commit()
        flash(f"Added {new_data}", category="success")
        return redirect(url_for('accounts.home', page=1))

    return render_template("accounts/add.html", form=form)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = Accounts.query.get(id)
    form = AccountsForm(obj=data_to_edit)
    form.account_type_id.choices = account_type_choices()
    if form.validate_on_submit():
        data_to_edit.data(form)
        data_to_edit.save_and_commit()
        flash(f"Edited {data_to_edit}", category="success")
        return redirect(url_for("accounts.home", page=1))
    return render_template("accounts/edit.html", form=form, id=id)


@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    data_to_delete = Accounts.query.get(id)
    data_to_delete.delete_and_commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for("accounts.home", page=1))


@bp.route("/export")
@login_required
def export():
    filename = Accounts().export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)


def account_type_choices():
    data = AccountType.query.order_by(AccountType.priority).all()
    data.insert(0, "")
    return data