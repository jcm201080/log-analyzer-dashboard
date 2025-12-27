from flask import Flask, render_template
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp   # 👈 login
# ---------------------------------

app = Flask(__name__)
app.secret_key = "clave-super-secreta"  # 👈 obligatorio para sesiones

# Blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

# ------------------------
# RUTAS PÚBLICAS
# ------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/box")
def box():
    return "Box (pendiente)"

@app.route("/registro")
def registro():
    return "Informe (pendiente)"

@app.route("/usuarios")
def usuarios():
    return "Usuarios (pendiente)"

@app.route("/descargar")
def descargar():
    return "Descarga (pendiente)"

# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
