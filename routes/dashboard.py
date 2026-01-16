from flask import Blueprint, render_template, jsonify, session
from pathlib import Path

from processing.analyzer import analyze
from processing.parser import parse_log
from processing.loader import load_network_hosts
from utils.security import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard_view():

    # 🟢 INICIALIZACIÓN POR DEFECTO (SOLO LA PRIMERA VEZ)
    if "active_log" not in session or "log_type" not in session:
        default_log = "data/Linux_2k.log"
        session["active_log"] = default_log
        session["log_type"] = "auth"

    # 🔑 Recuperar estado actual
    log_path = session.get("active_log")
    log_type = session.get("log_type")

    # 🛟 FALLBACK DE SEGURIDAD
    if log_path and not log_type:
        if "conn" in log_path:
            log_type = "network"
        else:
            log_type = "auth"

        session["log_type"] = log_type


    log_name = Path(log_path).name if log_path else "—"

    # =========================
    # 🔐 AUTH (solo si aplica)
    # =========================
    if log_type == "auth":
        results = analyze(log_path)
        _, log_stats = parse_log(log_path)
        total_attempts = results.get("total_intentos", 0)
    else:
        log_stats = {
            "total_lines": 0,
            "parsed_lines": 0,
            "discarded_lines": 0
        }
        total_attempts = 0


    # =========================
    # 🌐 NETWORK (solo si aplica)
    # =========================
    network_summary = None
    if log_type == "network":
        network_hosts = load_network_hosts()
        network_summary = {
            "hosts": len(network_hosts),
            "events": sum(h["total_events"] for h in network_hosts),
            "critical": sum(
                1 for h in network_hosts if h.get("risk_level") == "critical"
            )
        }

    return render_template(
        "dashboard.html",
        log_name=log_name,
        log_stats=log_stats,
        log_type=log_type,
        network_summary=network_summary,
        total_attempts=total_attempts
    )



@dashboard_bp.route("/api/dashboard")
@login_required
def dashboard_data():
    try:
        log_path = session.get("active_log")
        log_type = session.get("log_type")

        if log_type == "auth":
            data = analyze(log_path)
        else:
            data = {
                "total_intentos": 0,
                "hosts": [],
                "usuarios": [],
                "log_name": Path(log_path).name if log_path else "—",
                "fechas_incompletas": False
            }

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
