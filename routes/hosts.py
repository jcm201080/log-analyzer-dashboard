from flask import Blueprint, render_template, request, session, redirect, url_for
from pathlib import Path

from processing.analyzer import analyze
from processing.geoip import get_geo_info
from processing.loader import load_network_hosts

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

    # 🔍 Análisis AUTH
    results = analyze(log_path)
    raw_hosts = results.get("hosts", [])

    # 🌐 Cargar NETWORK
    network_hosts = load_network_hosts()

    # 🔐 Hosts AUTH
    hosts = [
        {
            "ip": h.get("host"),
            "intentos": h.get("intentos", 0),
            "log_type": "auth",
            **get_geo_info(h.get("host"))
        }
        for h in raw_hosts
    ]

    # 🌐 Hosts NETWORK
    network_hosts_normalized = [
        {
            "ip": h["ip"],
            "intentos": h["total_events"],
            "risk_level": h.get("risk_level"),
            "log_type": "network",
            **get_geo_info(h["ip"])
        }
        for h in network_hosts
    ]

    # 🔗 Unir ambos
    hosts.extend(network_hosts_normalized)

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

    # 🔍 AUTH
    results = analyze(log_path)
    raw_hosts = results.get("hosts", [])

    auth_host = next(
        (h for h in raw_hosts if h.get("host") == ip),
        None
    )

    # 🌐 NETWORK
    network_hosts = load_network_hosts()
    network_host = next(
        (h for h in network_hosts if h.get("ip") == ip),
        None
    )

    # ❌ No existe en ningún lado
    if not auth_host and not network_host:
        return render_template(
            "host_detail.html",
            error="Host no encontrado",
            ip=ip
        )

    geo = get_geo_info(ip)

    # 🧠 Construir vista final
    if auth_host:
        intentos = auth_host.get("intentos", 0)

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
            "log_type": "auth",
            **geo
        }

    else:
        # Network host
        intentos = network_host.get("total_events", 0)
        gravedad = network_host.get("risk_level", "unknown")

        host = {
            "ip": ip,
            "intentos": intentos,
            "gravedad": gravedad,
            "log_type": "network",
            **geo
        }

    return render_template(
        "host_detail.html",
        host=host,
        log_name=results.get("log_name")
    )