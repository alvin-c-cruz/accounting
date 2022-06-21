from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from .models import AccountType
from .forms import AccountTypeForm
from accounting import db

bp = Blueprint("account_type", __name__, template_folder="pages", url_prefix="/account_type")


@bp.route("/<int:page>")
@login_required
def home(page):
    account_types = AccountType.query.order_by(AccountType.priority).paginate(page=page, per_page=10)
    return render_template("account_type/home.html", account_types=account_types)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AccountTypeForm()
    if form.validate_on_submit():
        account_type = form.account_type.data
        classification = form.classification.data
        priority = form.priority.data

        if account_type == "":
            form.account_type.errors.append("Please type description of account type.")
        elif AccountType.query.filter_by(account_type=account_type).first():
            form.account_type.errors.append("Account type's description is already used.")
        else:
            new_data = AccountType(
                account_type=account_type,
                classification=classification,
                priority=priority,
                user_id=current_user.name
            )
            db.session.add(new_data)
            db.session.commit()
            flash(f"Added {new_data}", category="success")
            return redirect(url_for("account_type.home", page=1))
    return render_template("account_type/add.html", form=form)


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = AccountType.query.get(id)
    form = AccountTypeForm(obj=data_to_edit)
    if form.validate_on_submit():
        account_type = form.account_type.data
        classification = form.classification.data
        priority = form.priority.data

        if account_type == "":
            form.account_type.errors.append("Please type description of account type.")
        elif AccountType.query.filter(AccountType.account_type == account_type, AccountType.id != data_to_edit.id).first():
            form.account_type.errors.append("Account type's description is already used.")
        else:
            data_to_edit.account_type = account_type
            data_to_edit.classification = classification
            data_to_edit.priority = priority
            data_to_edit.user_id = current_user.name
            data_to_edit.date_modified = datetime.utcnow()
            db.session.commit()
            flash(f"Edited {data_to_edit}", category="success")
            return redirect(url_for("account_type.home", page=1))
    return render_template("account_type/edit.html", form=form, id=id)


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    data_to_delete = AccountType.query.get(id)
    db.session.delete(data_to_delete)
    db.session.commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for("account_type.home", page=1))


@bp.route("/export")
@login_required
def export():
    filename = AccountType().export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)

