from flask import Blueprint, render_template, request, session, redirect, url_for
from processing.analyzer import analyze

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
            "intentos": h.get("intentos", 0)
        }
        for h in raw_hosts
    ]

    return render_template(
        "hosts.html",
        hosts=hosts,
        time_range=time_range
    )
