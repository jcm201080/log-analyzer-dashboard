from flask import Blueprint, render_template
from utils.security import login_required

funcionamiento_bp = Blueprint(
    "funcionamiento",
    __name__,
    url_prefix="/funcionamiento"
)

@funcionamiento_bp.route("/")
@login_required
def funcionamiento():
    return render_template("funcionamiento.html")
