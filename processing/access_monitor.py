import sqlite3
import os
from datetime import datetime
from flask import request, session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "app_telemetry.db")


def init_db():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            user_agent TEXT,
            endpoint TEXT,
            method TEXT,
            status_code INTEGER,
            is_session_start INTEGER
        )

    """)

    conn.commit()
    conn.close()


def register_visit(req, status_code=200):
    try:
        if req.method != "GET":
            return

        if req.path.startswith("/static"):
            return

        if req.path == "/favicon.ico":
            return

        if "__debugger__" in req.path:
            return

        # 👇 NUEVO: contar solo primera visita de la sesión
        is_new_session = False

        if not session.get("visit_registered"):
            session["visit_registered"] = True
            is_new_session = True

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO visits (timestamp, ip, user_agent, endpoint, method, status_code, is_session_start)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            req.remote_addr,
            req.headers.get("User-Agent"),
            req.path,
            req.method,
            status_code,
            1 if is_new_session else 0
        ))

        conn.commit()
        conn.close()

    except Exception:
        pass

