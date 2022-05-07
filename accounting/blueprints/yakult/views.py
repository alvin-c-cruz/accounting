from flask import Blueprint, render_template, flash

from .forms import YakultForm

bp = Blueprint('yakult', __name__, template_folder="pages", url_prefix="/yakult")


@bp.route("/", methods=['GET', 'POST'])
def home():
    form = YakultForm()
    if form.validate_on_submit():
        age_group = form.age_group.data

        if age_group == "Adult":
            flash("You can drink up to two bottles of yakult per day.", "success")
        elif age_group == "Child":
            flash("You can drink one bottle of yakult per day.", "success")
        elif age_group == "Infant":
            flash("Please consult the pediatrician.", "error")

    return render_template("yakult/home.html", form=form)
