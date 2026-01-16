from flask import Blueprint, render_template, request, redirect, url_for, session
from pathlib import Path
from utils.security import login_required
from processing.log_type_detector import detect_log_type


upload_bp = Blueprint("upload", __name__)

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@upload_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_log():
    if request.method == "POST":
        file = request.files.get("logfile")

        if not file or file.filename == "":
            return render_template(
                "upload.html",
                error="No se ha seleccionado ningún archivo"
            )

        file_path = UPLOAD_DIR / file.filename
        file.save(file_path)

        # 🔑 Log activo para todo el sistema
        session["active_log"] = str(file_path)

        # 🧠 Detectar tipo de log
        log_type = detect_log_type(file_path)
        session["log_type"] = log_type

        return redirect(url_for("dashboard.dashboard_view"))


    return render_template("upload.html")
