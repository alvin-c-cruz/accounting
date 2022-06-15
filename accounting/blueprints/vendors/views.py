from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from datetime import datetime
from .models import Vendors
from .forms import VendorsForm
from accounting import db

bp = Blueprint("vendors", __name__, template_folder="pages", url_prefix="/vendors")


@bp.route("/<int:page>")
@login_required
def home(page):
    columns = [
            {"label": "Vendor", "key": "vendor_name"},
            {"label": "TIN", "key": "vendor_tin"}
        ]
    data = Vendors.query.order_by(Vendors.vendor_name).paginate(page=page, per_page=10)
    return render_template("vendors/home.html", data=data, columns=columns)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = VendorsForm()
    if form.validate_on_submit():
        new_data = Vendors()
        new_data.data(form)
        new_data.user_id = current_user.name
        db.session.add(new_data)
        db.session.commit()
        flash(f"Added {new_data}", category="success")
        return redirect(url_for("vendors.home", page=1))
    return render_template("vendors/add.html", form=form)


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = Vendors.query.get(id)
    form = VendorsForm(obj=data_to_edit)
    if form.validate_on_submit():
        data_to_edit.data(form)
        data_to_edit.date_modified = datetime.now()
        db.session.commit()
        flash(f"Edited {data_to_edit}", category="success")
        return redirect(url_for("vendors.home", page=1))
    return render_template("vendors/edit.html", form=form, id=id)


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    data_to_delete = Vendors.query.get(id)
    db.session.delete(data_to_delete)
    db.session.commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for("vendors.home", page=1))


@bp.route("/export")
@login_required
def export():
    filename = Vendors().export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)
