from flask import Blueprint, render_template, request, redirect, url_for, session



auth_bp = Blueprint("auth", __name__)

# Usuarios de ejemplo (para prácticas)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "analista": {"password": "analista123", "role": "viewer"},
    "jesus": {"password": "1234", "role": "admin"},
    "jcm": {"password": "1234", "role": "admin"}
}


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user in USERS and USERS[user]["password"] == pwd:
            session["user"] = user
            session["role"] = USERS[user]["role"]
            return redirect(url_for("dashboard.dashboard_view"))

        return "Credenciales incorrectas", 401

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
