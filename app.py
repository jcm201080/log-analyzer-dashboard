from flask import Flask, render_template
from dotenv import load_dotenv
import os

from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from routes.hosts import hosts_bp
from routes.export import export_bp
from routes.graficas import graficas_bp
from routes.upload import upload_bp
from routes.funcionamiento import funcionamiento_bp





# -------------------------------------------------
# Cargar variables de entorno
# -------------------------------------------------
load_dotenv()


# -------------------------------------------------
# Crear aplicación Flask
# -------------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


# -------------------------------------------------
# Registrar Blueprints
# -------------------------------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(hosts_bp)
app.register_blueprint(export_bp)
app.register_blueprint(graficas_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(funcionamiento_bp)


# -------------------------------------------------
# Rutas públicas
# -------------------------------------------------
@app.route("/")
def index() -> str:
    """Página de inicio pública."""
    return render_template("index.html")


# -------------------------------------------------
# Arranque de la aplicación
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)

