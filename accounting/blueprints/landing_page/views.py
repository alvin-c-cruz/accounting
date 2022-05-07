from flask import Blueprint, render_template


bp = Blueprint('landing_page', __name__, template_folder="pages")


@bp.route('/')
def home():
    return render_template('landing_page/home.html')
