from flask import Blueprint, render_template, jsonify, session
from processing.analyzer import analyze
from utils.security import login_required
from processing.parser import parse_log

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard_view():
    log_path = session.get("active_log")

    results, log_stats = parse_log(log_path)

    return render_template(
        "dashboard.html",
        log_stats=log_stats,
        log_name=log_path.split("/")[-1] if log_path else "—"
    )


@dashboard_bp.route("/api/dashboard")
@login_required
def dashboard_data():
    try:
        log_path = session.get("active_log")  # 👈 CLAVE
        data = analyze(log_path)

        # Limitar SOLO para el dashboard
        data["hosts"] = data.get("hosts", [])[:15]

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "total_intentos": 0,
            "hosts": [],
            "usuarios": [],
            "error": str(e)
        }), 500
