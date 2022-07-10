from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from datetime import datetime
from .models import Customers
from .forms import CustomerForm
from accounting import db

bp = Blueprint("customers", __name__, template_folder="pages", url_prefix="/customers")


@bp.route("/<int:page>")
@login_required
def home(page):
    columns = [
            {"label": "Customer", "key": "customer_name"},
            {"label": "TIN", "key": "customer_tin"}
        ]
    data = Customers.query.order_by(Customers.customer_name).paginate(page=page, per_page=10)
    return render_template("customers/home.html", data=data, columns=columns)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = CustomerForm()
    if form.validate_on_submit():
        validated = True
        customer_name = form.customer_name.data
        customer_tin = form.customer_tin.data

        if customer_name == "":
            form.customer_name.errors.append("Please type customer name.")
            validated = False
        elif Customers.query.filter_by(customer_name=customer_name).first():
            form.customer_name.errors.append("Customer name is already used.")
            validated = False

        if Customers.query.filter_by(customer_tin=customer_tin).first() and customer_tin:
            form.customer_tin.errors.append("TIN is already used.")
            validated = False

        if validated:
            new_data = Customers()
            new_data.customer_name = customer_name
            new_data.customer_tin = customer_tin
            new_data.user_id = current_user.id
            db.session.add(new_data)
            db.session.commit()
            flash(f"Added {new_data}", category="success")
            return redirect(url_for("customers.home", page=1))

    return render_template("customers/add.html", form=form)


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = Customers.query.get(id)
    form = CustomerForm(obj=data_to_edit)
    if form.validate_on_submit():
        validated = True
        customer_name = form.customer_name.data
        customer_tin = form.customer_tin.data

        if customer_name == "":
            form.customer_name.errors.append("Please type customer name.")
            validated = False
        elif Customers.query.filter(Customers.customer_name == customer_name, Customers.id != data_to_edit.id).first():
            form.customer_name.errors.append("Customer name is already used.")
            validated = False

        if Customers.query.filter(Customers.customer_tin == customer_tin, Customers.id != data_to_edit.id).first() \
                and customer_tin:
            form.customer_tin.errors.append("TIN is already used.")
            validated = False

        if validated:
            data_to_edit.customer_name = customer_name
            data_to_edit.customer_tin = customer_tin
            data_to_edit.user_id = current_user.id
            data_to_edit.date_modified = datetime.now()
            db.session.commit()
            flash(f"Edited {data_to_edit}", category="success")
            return redirect(url_for("customers.add"))
    return render_template("customers/edit.html", form=form, id=id)


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    data_to_delete = Customers.query.get(id)
    db.session.delete(data_to_delete)
    db.session.commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for("customers.home", page=1))


@bp.route("/export")
@login_required
def export():
    filename = Customers().export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)
