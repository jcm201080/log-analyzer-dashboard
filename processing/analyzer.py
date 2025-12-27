import pandas as pd
from processing.parser import parse_log


def calcular_gravedad(intentos):
    if intentos > 50:
        return "alta"      # 🔴
    elif intentos >= 10:
        return "media"     # 🟠
    else:
        return "baja"      # 🟢


def analyze():
    data = parse_log()
    df = pd.DataFrame(data)

    if df.empty:
        return {
            "total_intentos": 0,
            "hosts": [],
            "usuarios": []
        }

    # =========================
    # HOSTS
    # =========================
    rhosts = df["rhost"].value_counts()

    rhost_info = []
    for host, count in rhosts.items():
        rhost_info.append({
            "host": host,
            "intentos": int(count),
            "gravedad": calcular_gravedad(count)
        })

    # =========================
    # USUARIOS (FORMATO CORRECTO)
    # =========================
    users_count = df["user"].value_counts()

    usuarios = []
    for user, count in users_count.items():
        usuarios.append({
            "usuario": user,
            "intentos": int(count)
        })

    # =========================
    # EXPORTAR BLOCKLIST
    # =========================
    export_blocklist(rhost_info)

    return {
        "total_intentos": int(len(df)),
        "hosts": rhost_info,
        "usuarios": usuarios
    }


def export_blocklist(hosts, filename="blocklist.txt"):
    peligrosos = [h["host"] for h in hosts if h["gravedad"] == "alta"]

    with open(filename, "w", encoding="utf-8") as f:
        for host in peligrosos:
            f.write(f"{host}\n")
