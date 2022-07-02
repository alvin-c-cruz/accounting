from flask import Blueprint, render_template
from flask_login import login_required
from accounting import db

from .models import Company
from .forms import CompanyForm

bp = Blueprint("company", __name__, template_folder="pages", url_prefix="/company")


@bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    company = Company.query.get(1)
    if company is None:
        company = Company(company_name="Company Name")
        db.session.add(company)
        db.session.commit()

    form = CompanyForm(obj=company)

    if form.validate_on_submit():
        company.company_name = form.company_name.data

        company.disbursement_prepared = form.disbursement_prepared.data
        company.disbursement_check = form.disbursement_check.data
        company.disbursement_audited = form.disbursement_audited.data
        company.disbursement_approved = form.disbursement_approved.data

        db.session.commit()

    context = {
        "form": form
    }

    return render_template("company/home.html", **context)
