from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from datetime import datetime
from .models import Employees
from .forms import EmployeesForm
from accounting import db

bp = Blueprint("employees", __name__, template_folder="pages", url_prefix="/employees")


@bp.route("/<int:page>")
@login_required
def home(page):
    columns = [
            {"label": "Employee", "key": "employee_name"},
            {"label": "TIN", "key": "employee_tin"}
        ]
    data = Employees.query.order_by(Employees.employee_name).paginate(page=page, per_page=10)
    return render_template("employees/home.html", data=data, columns=columns)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = EmployeesForm()
    if form.validate_on_submit():
        validated = True
        employee_name = form.employee_name.data
        employee_tin = form.employee_tin.data

        if employee_name == "":
            form.employee_name.errors.append("Please type employee name.")
            validated = False
        elif Employees.query.filter_by(employee_name=employee_name).first():
            form.employee_name.errors.append("Employee name is already used.")
            validated = False

        if Employees.query.filter_by(employee_tin=employee_tin).first() and employee_tin:
            form.employee_tin.errors.append("TIN is already used.")
            validated = False

        if validated:
            new_data = Employees()
            new_data.employee_name = employee_name
            new_data.employee_tin = employee_tin if employee_tin else None

            new_data.user_id = current_user.id
            db.session.add(new_data)
            db.session.commit()
            flash(f"Added {new_data}", category="success")
            return redirect(url_for("employees.add"))

    return render_template("employees/add.html", form=form)


@bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    data_to_edit = Employees.query.get(id)
    form = EmployeesForm(obj=data_to_edit)
    if form.validate_on_submit():
        validated = True
        employee_name = form.employee_name.data
        employee_tin = form.employee_tin.data

        if employee_name == "":
            form.employee_name.errors.append("Please type employee name.")
            validated = False
        elif Employees.query.filter(Employees.employee_name == employee_name, Employees.id != data_to_edit.id).first():
            form.employee_name.errors.append("Employee name is already used.")
            validated = False

        if Employees.query.filter(Employees.employee_tin == employee_tin, Employees.id != data_to_edit.id).first() \
                and employee_tin:
            form.employee_tin.errors.append("TIN is already used.")
            validated = False

        if validated:
            data_to_edit.employee_name = employee_name
            if employee_tin:
                data_to_edit.employee_tin = employee_tin
            data_to_edit.user_id = current_user.id
            data_to_edit.date_modified = datetime.now()
            db.session.commit()
            flash(f"Edited {data_to_edit}", category="success")
            return redirect(url_for("employees.home", page=1))
    return render_template("employees/edit.html", form=form, id=id)


@bp.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    data_to_delete = Employees.query.get(id)
    db.session.delete(data_to_delete)
    db.session.commit()
    flash(f"Deleted {data_to_delete}", category="success")
    return redirect(url_for("employees.home", page=1))


@bp.route("/export")
@login_required
def export():
    filename = Employees().export()
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)
