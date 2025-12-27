from flask import Blueprint, render_template, jsonify
from processing.analyzer import analyze
from utils.security import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard_view():
    return render_template("dashboard.html")

@dashboard_bp.route("/api/dashboard")
@login_required
def dashboard_data():
    try:
        data = analyze()
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "total_intentos": 0,
            "hosts": [],
            "usuarios": [],
            "error": str(e)
        }), 500
