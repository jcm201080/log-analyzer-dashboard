from flask import Blueprint, render_template
from pathlib import Path
from datetime import datetime
from utils.security import login_required

from processing.simulator import generate_simulated_log_file

simulacion_bp = Blueprint("simulacion", __name__)

@simulacion_bp.route("/simulacion")
@login_required
def simulacion():
    filename = generate_simulated_log_file()

    return render_template(
        "simulacion.html",
        filename=filename
    )

