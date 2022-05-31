from flask import Blueprint, render_template
from flask_login import login_required
from .models import Accounts
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
    return "Add Account"


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    return f"Edit {id}"


@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    return f"Delete {id}"


@bp.route("/export")
@login_required
def export():
    return "Export Accounts"