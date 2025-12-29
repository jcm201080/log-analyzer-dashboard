from flask import Blueprint, render_template, request, session, redirect, url_for
from processing.analyzer import analyze
from processing.geoip import get_geo_info

hosts_bp = Blueprint("hosts", __name__)

@hosts_bp.route("/hosts")
def hosts():
    # 🔐 Protección
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    # ⏱️ Filtro temporal
    time_range = request.args.get("range", "24h")

    # 🔍 Análisis
    results = analyze()
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
        time_range=time_range
    )



# detalle de un host específico
@hosts_bp.route("/hosts/<path:ip>")
def host_detail(ip):
    # 🔐 Protección
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    # 🔍 Ejecutar análisis
    results = analyze()
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
        host=host
    )
