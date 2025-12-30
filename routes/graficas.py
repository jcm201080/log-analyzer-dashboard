from flask import Blueprint, render_template
from utils.security import login_required

graficas_bp = Blueprint("graficas", __name__)

@graficas_bp.route("/graficas")
@login_required
def graficas():
    return render_template("graficas.html")
