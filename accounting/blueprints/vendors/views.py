from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from datetime import datetime
from .models import Vendors
from .forms import VendorsForm

bp = Blueprint("vendors", __name__, template_folder="pages", url_prefix="/vendors")


@bp.route("/<int:page>")
@login_required
def home(page):
    obj = Vendors()
    data = Vendors.query.order_by(Vendors.vendor_name).paginate(page=page, per_page=10)
    return render_template(
        obj.home_html,
        obj=obj,
        data=data,
        columns=[
            {"label": "Vendor", "key": "vendor_name"},
            {"label": "TIN", "key": "vendor_tin"}
        ]
    )


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    obj = Vendors()
    form = VendorsForm()
    if form.validate_on_submit():
        new_data = obj
        new_data.data(form)
        new_data.user_id = current_user.name
        new_data.save_and_commit()
        flash(f"Added {new_data}", category="success")
        return redirect(url_for(obj.home_route, page=1))
    return render_template(
        obj.add_html,
        obj=obj,
        form=form
    )


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    obj = Vendors()
    data_to_edit = Vendors.query.get(id)
    form = VendorsForm(obj=data_to_edit)
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
    obj = Vendors()
    data_to_delete = Vendors.query.get(id)
    data_to_delete.delete_and_commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for(obj.home_route, page=1))


@bp.route("/export")
@login_required
def export():
    obj = Vendors()
    filename = obj.export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)
