from flask import Flask, render_template
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp   # 👈 login
from routes.hosts import hosts_bp  # 👈 nueva ruta hosts
from routes.export import export_bp  # 👈 nueva ruta export
from routes.graficas import graficas_bp
from routes.upload import upload_bp  # 👈 nueva ruta upload
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno desde .env
print("SECRET_KEY:", os.getenv("SECRET_KEY"))  # Verificar carga de variable de entorno
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



app.register_blueprint(hosts_bp)

app.register_blueprint(export_bp)

app.register_blueprint(graficas_bp)

app.register_blueprint(upload_bp)

# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
