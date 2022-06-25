from flask import Blueprint, render_template, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from accounting import db, incrementer

from .models import Disbursements, DisbursementsEntry
from .forms import DisbursementsForm
from .. vendors import Vendors
from .. accounts import Accounts

bp = Blueprint("disbursements", __name__, template_folder="pages", url_prefix="/disbursements")


@bp.route("/<int:page>")
@login_required
def home(page):
    cd = Disbursements.query.get(1)
    print(cd)
    print(cd.entries)
    context = {
        "data": Disbursements.query.order_by(Disbursements.disbursement_number).paginate(page=page, per_page=10),
        "columns": [
            {"label": "Record Date", "key": "record_date"},
            {"label": "Bank Date", "key": "bank_date"},
            {"label": "CD Number", "key": "disbursement_number"},
            {"label": "Check Number", "key": "check_number"},
            {"label": "Vendor", "key": "vendor_id"},
        ]
    }
    return render_template("disbursements/home.html", **context)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = DisbursementsForm()
    form.vendor_id.choices = vendor_choices()
    for entry in form.entries:
        entry.account_id.choices = account_choices()

    if form.validate_on_submit():
        record_date = form.record_date.data
        bank_date = form.bank_date.data
        disbursement_number = form.disbursement_number.data
        check_number = form.check_number.data
        notes = form.notes.data
        vendor_id = form.vendor_id.data

        if not record_date:
            form.record_date.errors.append("Please type record date.")

        if not disbursement_number:
            form.disbursement_number.errors.append("Please type CD number.")
        elif Disbursements.query.filter(Disbursements.disbursement_number==disbursement_number).first():
            form.disbursement_number.errors.append("CD number is already used.")

        if not check_number:
            form.check_number.errors.append("Please type check number.")
        elif Disbursements.query.filter(Disbursements.check_number==check_number).first():
            form.check_number.errors.append("Check number is already used.")

        if not vendor_id:
            form.vendor_id.errors.append("Please select a vendor.")

        if not form.errors:
            new_data = Disbursements(
                record_date=record_date,
                bank_date=bank_date,
                disbursement_number=disbursement_number,
                check_number=check_number,
                notes=notes,
                vendor_id=vendor_id,
                user_id=current_user.id
            )

            for i, entry in enumerate(form.entries):
                if entry.account_id.data == "":
                    continue
                new_entry = DisbursementsEntry(
                    disbursement_id=new_data.id,
                    account_id=entry.account_id.data,
                    debit=entry.debit.data,
                    credit=entry.credit.data,
                    notes=entry.notes.data
                )
                new_data.entries.append(new_entry)

            db.session.add(new_data)
            db.session.commit()

            flash(f"Added {new_data}", category="success")
            return redirect(url_for("disbursements.home", page=1))

    else:
        form.record_date.data = datetime.today()
        last_entry = Disbursements.query.order_by(-Disbursements.id).first()
        if last_entry:
            form.disbursement_number.data = incrementer(last_entry.disbursement_number)

    context = {
        "form": form
    }
    return render_template("disbursements/add.html", **context)


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = Disbursements.query.filter_by(id=id).first()
    form = DisbursementsForm(obj=data_to_edit)
    form.entries(obj=data_to_edit.disbursements)
    form.vendor_id.choices = vendor_choices()
    for entry in form.entries:
        entry.account_id.choices = account_choices()
    if form.validate_on_submit():
        data_to_edit.data(form)
        data_to_edit.date_modified = datetime.now()
        data_to_edit.save_and_commit()
        flash(f"Edited {data_to_edit}", category="success")
        return redirect(url_for("disbursements.home", page=1))
    return render_template(
        "disbursements/edit.html",
        form=form,
        id=id
    )


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    obj = Disbursements()
    data_to_delete = Disbursements.query.get(id)
    entry_to_delete = DisbursementsEntry.query.filter_by(disbursement_id=data_to_delete.__repr__()).all()
    for entry in entry_to_delete:
        entry.delete_and_commit()

    data_to_delete.delete_and_commit()

    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for(obj.home_route, page=1))


@bp.route("/export")
@login_required
def export():
    obj = Disbursements()
    filename = obj.export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)


def vendor_choices():
    data = [(row.id, row.vendor_name) for row in Vendors.query.order_by(Vendors.vendor_name).all()]
    data.insert(0, ("", ""))
    return data


def account_choices():
    data = [(row.id, row) for row in Accounts.query.order_by(Accounts.account_number).all()]
    data.insert(0, ("", ""))
    return data


@bp.route("/view")
@login_required
def view():
    data = [x.as_json() for x in DisbursementsEntry.query.all()]
    return jsonify(data)
