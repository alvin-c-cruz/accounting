from flask import Blueprint, flash, current_app, send_file
from flask_login import login_required
import os


bp = Blueprint('transition', __name__, url_prefix="/transition")


@bp.route("/")
@login_required
def home():
    filename = os.path.join(current_app.instance_path, "data.db")
    flash("Downloaded database.")
    return send_file('{}'.format(filename), as_attachment=True, cache_timeout=0)

