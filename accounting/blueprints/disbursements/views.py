from flask import Blueprint, render_template, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta


from accounting import db, incrementer, to_float, balance_check

from .models import Disbursements, DisbursementsEntry
from .forms import DisbursementsForm, JournalDateRange
from .extentions import create_journal

from .. vendors import vendor_choices
from .. accounts import account_choices

bp = Blueprint("disbursements", __name__, template_folder="pages", url_prefix="/disbursements")


@bp.route("/<int:page>", methods=["GET", "POST"])
@login_required
def home(page):
    journal_form = JournalDateRange()
    if journal_form.validate_on_submit():
        date_from = journal_form.date_from.data
        date_to = journal_form.date_to.data

        if date_from is None:
            flash("Beginning date is required.", category="error")

        elif date_to is None:
            flash("Ending date is required.", category="error")

        elif date_from > date_to:
            flash("Beginning date cannot be later than ending date.", category="error")

        else:
            date_from = datetime(date_from.year, date_from.month, date_from.day)
            date_to = datetime(date_to.year, date_to.month, date_to.day)

            data = Disbursements.query.filter(
                Disbursements.record_date >= date_from, Disbursements.record_date <= date_to
                ).order_by(Disbursements.disbursement_number).all()

            if data:
                filename = create_journal(data, current_app, date_from, date_to)
                return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)
            else:
                flash("No data within the date range.", category="error")

    else:
        today = datetime.today()
        first_day = datetime(today.year, today.month, 1)
        last_day = datetime(today.year, today.month + 1, 1) if today.month != 12 else datetime(today.year + 1, 1, 1)
        last_day -= timedelta(days=1)

        journal_form.date_from.data = first_day
        journal_form.date_to.data = last_day

    context = {
        "data": Disbursements.query.order_by(Disbursements.disbursement_number.desc()).paginate(page=page, per_page=10),
        "columns": [
            {"label": "Record Date", "key": "record_date"},
            {"label": "Bank Date", "key": "bank_date"},
            {"label": "CD Number", "key": "disbursement_number"},
            {"label": "Check Number", "key": "check_number"},
            {"label": "Vendor", "key": "vendor"},
        ],
        "journal_form": journal_form
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
        validate(form)

        if not form.errors:
            new_data = Disbursements(
                record_date=form.record_date.data,
                bank_date=form.bank_date.data,
                disbursement_number=form.disbursement_number.data,
                check_number=form.check_number.data,
                notes=form.notes.data,
                vendor_id=form.vendor_id.data,
                user_id=current_user.id
            )

            for i, entry in enumerate(form.entries):
                if entry.account_id.data == "":
                    continue
                new_entry = DisbursementsEntry(
                    disbursement_id=new_data.id,
                    account_id=entry.account_id.data,
                    debit=to_float(entry.debit.data),
                    credit=to_float(entry.credit.data),
                    notes=entry.notes.data
                )
                new_data.entries.append(new_entry)

            total_debit, total_credit = balance_check(form.entries)
            if total_debit == total_credit:
                db.session.add(new_data)
                db.session.commit()
                flash(f"Added {new_data}", category="success")
                return redirect(url_for("disbursements.add"))
            else:
                total_debit = "{:,.2f}".format(total_debit)
                total_credit = "{:,.2f}".format(total_credit)
                flash(f"Entry not balanced. Debit [{total_debit}], Credit [{total_credit}]", category="error")

    else:
        form.record_date.data = datetime.today()
        last_entry = Disbursements.query.order_by(-Disbursements.id).first()
        if last_entry:
            form.disbursement_number.data = incrementer(last_entry.disbursement_number)
            form.check_number.data = incrementer(last_entry.check_number)

    context = {
        "form": form
    }
    return render_template("disbursements/add.html", **context)


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = Disbursements.query.filter_by(id=id).first()
    form = DisbursementsForm(obj=data_to_edit)
    form.vendor_id.choices = vendor_choices()
    for entry in form.entries:
        entry.account_id.choices = account_choices()
    if form.validate_on_submit():
        validate(form, id)

        if not form.errors:
            data_to_edit.data(form)
            data_to_edit.user_id = current_user.id
            data_to_edit.date_modified = datetime.utcnow()

            for_deletion = []

            for i, entry in enumerate(form.entries):
                entry_id = entry.entry_id.data
                account_id = entry.account_id.data
                debit = to_float(entry.debit.data)
                credit = to_float(entry.credit.data)
                notes = entry.notes.data

                if entry_id:
                    if not account_id and not notes and debit == 0 and credit == 0:
                        for data in data_to_edit.entries:
                            if data.entry_id == int(entry_id):
                                for_deletion.append(data)
                                break

                    else:
                        for data in data_to_edit.entries:
                            if data.entry_id == int(entry_id):
                                data.account_id = account_id
                                data.debit = to_float(debit)
                                data.credit = to_float(credit)
                                data.notes = notes
                                break
                else:
                    if not account_id and not notes and debit == 0 and credit == 0:
                        continue

                    new_entry = DisbursementsEntry(
                        disbursement_id=data_to_edit.id,
                        account_id=account_id,
                        debit=to_float(debit),
                        credit=to_float(credit),
                        notes=notes
                    )
                    data_to_edit.entries.append(new_entry)

            for entry in for_deletion:
                db.session.delete(entry)

            total_debit, total_credit = balance_check(form.entries)
            if total_debit == total_credit:
                db.session.commit()
                flash(f"Edited {data_to_edit}", category="success")
                return redirect(url_for("disbursements.home", page=1))
            else:
                total_debit = "{:,.2f}".format(total_debit)
                total_credit = "{:,.2f}".format(total_credit)
                flash(f"Entry not balanced. Debit [{total_debit}], Credit [{total_credit}]", category="error")

    context = {
        "form": form,
        "id": id
    }

    return render_template("disbursements/edit.html", **context)


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    data_to_delete = Disbursements.query.get_or_404(id)

    for entry in data_to_delete.entries:
        db.session.delete(entry)

    db.session.delete(data_to_delete)
    db.session().expire_on_commit = False
    db.session.commit()

    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for("disbursements.home", page=1))


def validate(form, id=None):
    record_date = form.record_date.data
    disbursement_number = form.disbursement_number.data
    check_number = form.check_number.data
    vendor_id = form.vendor_id.data

    if not record_date:
        form.record_date.errors.append("Please type record date.")

    if not vendor_id:
        form.vendor_id.errors.append("Please select a vendor.")

    if id:
        if not disbursement_number:
            form.disbursement_number.errors.append("Please type CD number.")
        elif Disbursements.query.filter(
                Disbursements.disbursement_number == disbursement_number,
                Disbursements.id != id).first():
            form.disbursement_number.errors.append("CD number is already used.")

        if not check_number:
            form.check_number.errors.append("Please type check number.")
        elif Disbursements.query.filter(
                Disbursements.check_number == check_number,
                Disbursements.id != id).first():
            form.check_number.errors.append("Check number is already used.")

    else:
        if not disbursement_number:
            form.disbursement_number.errors.append("Please type CD number.")
        elif Disbursements.query.filter(Disbursements.disbursement_number == disbursement_number).first():
            form.disbursement_number.errors.append("CD number is already used.")

        if not check_number:
            form.check_number.errors.append("Please type check number.")
        elif Disbursements.query.filter(Disbursements.check_number == check_number).first():
            form.check_number.errors.append("Check number is already used.")


