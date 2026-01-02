from flask import Blueprint, render_template, session
from utils.security import login_required
from processing.analyzer import analyze
from pathlib import Path

graficas_bp = Blueprint("graficas", __name__)

@graficas_bp.route("/graficas")
@login_required
def graficas():
    # 📄 Log activo
    log_path = session.get("active_log")
    if log_path:
        log_path = Path(log_path)

    results = analyze(log_path)

    return render_template(
        "graficas.html",
        log_name=results.get("log_name")
    )
