from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    Response
)

from processing.analyzer import analyze
from processing.geoip import get_geo_info

import csv
import json
from io import StringIO


export_bp = Blueprint("export", __name__)

# =====================================================
# PÁGINA DE EXPORTACIÓN
# =====================================================
@export_bp.route("/export")
def export():
    # 🔐 Protección por sesión
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    # ⏱️ Filtro temporal (futuro)
    time_range = request.args.get("range", "24h")

    # 📄 Log activo
    log_path = session.get("active_log")

    results = analyze(log_path)

    return render_template(
        "export.html",
        time_range=time_range,
        log_name=results.get("log_name")
    )


# =====================================================
# EXPORTAR CSV
# =====================================================
@export_bp.route("/export/csv")
def export_csv():
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    # 📄 Log activo
    log_path = session.get("active_log")

    # 🔍 Ejecutar análisis
    results = analyze(log_path)
    hosts = results.get("hosts", [])

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["ip", "pais", "region", "ciudad", "intentos"])

    for h in hosts:
        ip = h.get("host")
        geo = get_geo_info(ip)

        writer.writerow([
            ip,
            geo["country"],
            geo["region"],
            geo["city"],
            h.get("intentos", 0)
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )
    response.headers["Content-Disposition"] = (
        "attachment; filename=hosts_atacantes.csv"
    )

    return response



# =====================================================
# EXPORTAR JSON
# =====================================================
@export_bp.route("/export/json")
def export_json():
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    # 📄 Log activo
    log_path = session.get("active_log")

    # 🔍 Ejecutar análisis
    results = analyze(log_path)
    hosts = results.get("hosts", [])

    data = [
        {
            "ip": h.get("host"),
            **get_geo_info(h.get("host")),
            "intentos": h.get("intentos", 0)
        }
        for h in hosts
    ]

    response = Response(
        json.dumps(data, indent=2, ensure_ascii=False),
        mimetype="application/json"
    )
    response.headers["Content-Disposition"] = (
        "attachment; filename=hosts_atacantes.json"
    )

    return response

