from flask import Blueprint, render_template
import sqlite3
import os
from datetime import datetime
from utils.security import login_required, role_required

telemetry_bp = Blueprint("telemetry", __name__, url_prefix="/telemetry")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "app_telemetry.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@telemetry_bp.route("/")
@login_required
@role_required("admin")
def telemetry_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # MÉTRICAS GENERALES
    # ==========================

    cursor.execute("SELECT COUNT(*) as total FROM visits")
    total_visits = cursor.fetchone()["total"]

    today = datetime.utcnow().date().isoformat()
    cursor.execute("""
        SELECT COUNT(*) as today_total
        FROM visits
        WHERE date(timestamp) = ?
    """, (today,))
    today_visits = cursor.fetchone()["today_total"]

    # Sesiones reales
    cursor.execute("""
        SELECT COUNT(*) as total_sessions
        FROM visits
        WHERE is_session_start = 1
    """)
    total_sessions = cursor.fetchone()["total_sessions"]

    # ==========================
    # TOP IPs
    # ==========================

    cursor.execute("""
        SELECT ip, COUNT(*) as count
        FROM visits
        GROUP BY ip
        ORDER BY count DESC
        LIMIT 5
    """)
    top_ips = cursor.fetchall()

    # ==========================
    # TOP ENDPOINTS
    # ==========================

    cursor.execute("""
        SELECT endpoint, COUNT(*) as count
        FROM visits
        GROUP BY endpoint
        ORDER BY count DESC
        LIMIT 5
    """)
    top_endpoints = cursor.fetchall()

    # ==========================
    # ERRORES 404 ÚLTIMOS 7 DÍAS
    # ==========================

    cursor.execute("""
        SELECT date(timestamp) as day, COUNT(*) as count
        FROM visits
        WHERE status_code = 404
        AND date(timestamp) >= date('now', '-7 days')
        GROUP BY day
        ORDER BY day ASC
    """)
    errors_404 = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) as total_404
        FROM visits
        WHERE status_code = 404
    """)
    total_404 = cursor.fetchone()["total_404"]

    # ==========================
    # 🚨 DETECCIÓN IP ACTIVA (5 MIN)
    # ==========================

    cursor.execute("""
        SELECT ip, COUNT(*) as count
        FROM visits
        WHERE timestamp >= datetime('now', '-5 minutes')
        GROUP BY ip
        HAVING count > 20
        ORDER BY count DESC
    """)
    suspicious_ips = cursor.fetchall()

    possible_scan = len(suspicious_ips) > 0

    conn.close()

    return render_template(
        "telemetry.html",
        total_visits=total_visits,
        today_visits=today_visits,
        total_sessions=total_sessions,
        top_ips=top_ips,
        top_endpoints=top_endpoints,
        errors_404=errors_404,
        total_404=total_404,
        suspicious_ips=suspicious_ips,
        possible_scan=possible_scan
    )



@telemetry_bp.route("/public")
@login_required
def telemetry_public():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM visits")
    total_visits = cursor.fetchone()["total"]

    today = datetime.utcnow().date().isoformat()
    cursor.execute("""
        SELECT COUNT(*) as today_total
        FROM visits
        WHERE date(timestamp) = ?
    """, (today,))
    today_visits = cursor.fetchone()["today_total"]

    cursor.execute("""
        SELECT endpoint, COUNT(*) as count
        FROM visits
        GROUP BY endpoint
        ORDER BY count DESC
        LIMIT 5
    """)
    top_endpoints = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(DISTINCT endpoint) as total_endpoints
        FROM visits
    """)

    total_distinct_endpoints = cursor.fetchone()["total_endpoints"]


    cursor.execute("""
        SELECT date(timestamp) as day, COUNT(*) as count
        FROM visits
        WHERE date(timestamp) >= date('now', '-7 days')
        GROUP BY day
        ORDER BY day ASC
    """)


    visits_per_day = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) as total_days
        FROM (
            SELECT DISTINCT date(timestamp) as day
            FROM visits
        )
    """)

    total_days = cursor.fetchone()["total_days"]

    average_per_day = 0
    if total_days > 0:
        average_per_day = round(total_visits / total_days, 2)

    # Total visitas reales (inicio de sesión)
    cursor.execute("""
        SELECT COUNT(*) as total_sessions
        FROM visits
        WHERE is_session_start = 1
    """)
    total_sessions = cursor.fetchone()["total_sessions"]

    # Visitas reales últimos 7 días
    cursor.execute("""
        SELECT COUNT(*) as sessions_last_7_days
        FROM visits
        WHERE is_session_start = 1
        AND date(timestamp) >= date('now', '-7 days')
    """)
    sessions_last_7_days = cursor.fetchone()["sessions_last_7_days"]

    # Visitas reales hoy
    cursor.execute("""
        SELECT COUNT(*) as sessions_today
        FROM visits
        WHERE is_session_start = 1
        AND date(timestamp) = date('now')
    """)
    sessions_today = cursor.fetchone()["sessions_today"]

    # Sesiones últimos 7 días
    cursor.execute("""
        SELECT date(timestamp) as day, COUNT(*) as count
        FROM visits
        WHERE is_session_start = 1
        AND date(timestamp) >= date('now', '-7 days')
        GROUP BY day
        ORDER BY day ASC
    """)

    sessions_per_day = cursor.fetchall()



        


    conn.close()

    return render_template(
        "telemetry_public.html",
        total_visits=total_visits,
        today_visits=today_visits,
        top_endpoints=top_endpoints,
        visits_per_day=visits_per_day,
        total_distinct_endpoints=total_distinct_endpoints,
        average_per_day=average_per_day,
        total_sessions=total_sessions,
        sessions_last_7_days=sessions_last_7_days,
        sessions_today=sessions_today,
        sessions_per_day=sessions_per_day
    )

