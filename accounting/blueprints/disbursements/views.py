from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from datetime import datetime
from .models import Disbursements, DisbursementsEntry
from .forms import DisbursementsForm
from .. vendors import Vendors
from .. accounts import Accounts

bp = Blueprint("disbursements", __name__, template_folder="pages", url_prefix="/disbursements")
obj = Disbursements()


@bp.route("/<int:page>")
@login_required
def home(page):
    data = Disbursements.query.order_by(Disbursements.disbursement_number).paginate(page=page, per_page=10)
    return render_template(
        obj.home_html,
        obj=obj,
        data=data,
        columns=[
            {"label": "Record Date", "key": "record_date"},
            {"label": "Bank Date", "key": "bank_date"},
            {"label": "CD Number", "key": "disbursement_number"},
            {"label": "Check Number", "key": "check_number"},
            {"label": "Vendor", "key": "vendor_id"},
        ]
    )


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = DisbursementsForm()
    form.vendor_id.choices = vendor_choices()
    for entry in form.entries:
        entry.account_id.choices = account_choices()

    if form.validate_on_submit():
        new_data = obj
        new_data.data(form)
        new_data.user_id = current_user.name
        new_data.save()
        for i, entry in enumerate(form.entries):
            if entry.account_id == "":
                continue
            new_entry = DisbursementsEntry()
            entry.disbursement_id.data = new_data.__repr__()
            new_entry.data(entry)
            new_entry.save()
        new_data.commit()

        flash(f"Added {new_data}", category="success")
        return redirect(url_for(obj.home_route, page=1))

    else:
        form.record_date.data = datetime.today()
    return render_template(
        obj.add_html,
        obj=obj,
        form=form
    )


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = obj.query.get(id)
    form = DisbursementsForm(obj=data_to_edit)
    form.vendor_id.choices = vendor_choices()
    for entry in form.entries:
        entry.account_id.choices = account_choices()
    if form.validate_on_submit():
        data_to_edit.data(form)
        data_to_edit.date_modified = datetime.now()
        data_to_edit.save_and_commit()
        flash(f"Edited {data_to_edit}", category="success")
        return redirect(url_for(obj.home_route, page=1))
    return render_template(
        obj.edit_html,
        form=form,
        id=id,
        obj=obj
    )


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    data_to_delete = Disbursements.query.get(id)
    data_to_delete.delete_and_commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for(obj.home_route, page=1))


@bp.route("/export")
@login_required
def export():
    filename = obj.export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)


def vendor_choices():
    data = Vendors.query.order_by(Vendors.vendor_name).all()
    data.insert(0, "")
    return data


def account_choices():
    data = Accounts.query.order_by(Accounts.account_number).all()
    data.insert(0, "")
    return data