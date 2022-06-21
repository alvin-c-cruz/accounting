from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from datetime import datetime

from accounting import db

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
        validated = True
        account_number = form.account_number.data
        account_title = form.account_title.data
        account_type_id = form.account_type_id.data

        if account_number == "":
            form.account_number.errors.append("Please type account number.")
            validated = False
        elif Accounts.query.filter_by(account_number=account_number).first():
            form.account_number.errors.append("Account number is already in use.")
            validated = False

        if account_title == "":
            form.account_title.errors.append("Please type account title.")
            validated = False
        elif Accounts.query.filter_by(account_title=account_title).first():
            form.account_title.errors.append("Account title is already in use.")
            validated = False

        if validated:
            new_data = Accounts(
                account_number=account_number,
                account_title=account_title,
                account_type_id=account_type_id,
                user_id=current_user.name
            )
            db.session.add(new_data)
            db.session.commit()
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
        validated = True
        account_number = form.account_number.data
        account_title = form.account_title.data
        account_type_id = form.account_type_id.data

        if account_number == "":
            form.account_number.errors.append("Please type account number.")
            validated = False
        elif Accounts.query.filter(Accounts.account_number == account_number, Accounts.id != data_to_edit.id).first():
            form.account_number.errors.append("Account number is already in use.")
            validated = False

        if account_title == "":
            form.account_title.errors.append("Please type account title.")
            validated = False
        elif Accounts.query.filter(Accounts.account_title == account_title, Accounts.id != data_to_edit.id).first():
            form.account_title.errors.append("Account title is already in use.")
            validated = False

        if validated:
            data_to_edit.account_number = account_number
            data_to_edit.account_title = account_title
            data_to_edit.account_type_id = account_type_id
            data_to_edit.user_id = current_user.name
            data_to_edit.date_modified = datetime.now()
            db.session.commit()
            flash(f"Edited {data_to_edit}", category="success")
            return redirect(url_for("accounts.home", page=1))
    return render_template("accounts/edit.html", form=form, id=id)


@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    data_to_delete = Accounts.query.get(id)
    db.session.delete(data_to_delete)
    db.session.commit()
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