from flask import Blueprint, render_template, request, session, redirect, url_for
from pathlib import Path
from processing.analyzer import analyze
from processing.geoip import get_geo_info

hosts_bp = Blueprint("hosts", __name__)

@hosts_bp.route("/hosts")
def hosts():
    # 🔐 Protección
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    # ⏱️ Filtro temporal (futuro)
    time_range = request.args.get("range", "24h")

    # 📄 Log activo
    log_path = session.get("active_log")
    if log_path:
        log_path = Path(log_path)

    # 🔍 Análisis
    results = analyze(log_path)
    raw_hosts = results.get("hosts", [])

    hosts = [
        {
            "ip": h.get("host"),
            "intentos": h.get("intentos", 0),
            **get_geo_info(h.get("host"))
        }
        for h in raw_hosts
    ]

    return render_template(
        "hosts.html",
        hosts=hosts,
        time_range=time_range,
        log_name=results.get("log_name")
    )
@hosts_bp.route("/hosts/<path:ip>")
def host_detail(ip):
    # 🔐 Protección
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    # 📄 Log activo
    log_path = session.get("active_log")
    if log_path:
        log_path = Path(log_path)

    # 🔍 Ejecutar análisis
    results = analyze(log_path)
    raw_hosts = results.get("hosts", [])

    # Buscar el host concreto
    host_data = next(
        (h for h in raw_hosts if h.get("host") == ip),
        None
    )

    if not host_data:
        return render_template(
            "host_detail.html",
            error="Host no encontrado",
            ip=ip
        )

    geo = get_geo_info(ip)
    intentos = host_data.get("intentos", 0)

    # Calcular gravedad
    if intentos > 20:
        gravedad = "Alta"
    elif intentos > 10:
        gravedad = "Media"
    else:
        gravedad = "Baja"

    host = {
        "ip": ip,
        "intentos": intentos,
        "gravedad": gravedad,
        **geo
    }

    return render_template(
        "host_detail.html",
        host=host,
        log_name=results.get("log_name")
    )
