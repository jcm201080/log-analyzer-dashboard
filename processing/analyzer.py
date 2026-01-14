import os
import pandas as pd
from pathlib import Path
from processing.parser import parse_log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")



def calcular_gravedad(intentos):
    if intentos > 50:
        return "alta"      # 🔴
    elif intentos >= 10:
        return "media"     # 🟠
    else:
        return "baja"      # 🟢


def analyze(log_path=None):
    """
    Analiza el log activo.
    Si no se indica ruta, se usa el log por defecto del parser.
    """

    # =========================
    # PARSEAR LOG
    # =========================
    data, _ = parse_log(log_path)
    df = pd.DataFrame(data)


    # =========================
    # NOMBRE DEL LOG
    # =========================
    if log_path:
        log_name = Path(log_path).name
    else:
        log_name = "OpenSSH_2k.log"

    # =========================
    # FECHAS INCOMPLETAS
    # =========================
    fechas_incompletas = False
    if not df.empty and "date" in df.columns:
        # Los logs no incluyen año → incompletas
        fechas_incompletas = True

    # =========================
    # DATAFRAME VACÍO
    # =========================
    if df.empty:
        return {
            "total_intentos": 0,
            "hosts": [],
            "usuarios": [],
            "log_name": log_name,
            "fechas_incompletas": fechas_incompletas
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
    # USUARIOS
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

    # =========================
    # RESULTADO FINAL
    # =========================
    return {
        "total_intentos": int(len(df)),
        "hosts": rhost_info,
        "usuarios": usuarios,
        "log_name": log_name,
        "fechas_incompletas": fechas_incompletas
    }


def export_blocklist(hosts, filename=None):
    if filename is None:
        filename = os.path.join(DATA_DIR, "blocklist.txt")

    peligrosos = [h["host"] for h in hosts if h["gravedad"] == "alta"]

    with open(filename, "w", encoding="utf-8") as f:
        for host in peligrosos:
            f.write(f"{host}\n")

