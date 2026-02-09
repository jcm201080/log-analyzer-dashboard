from datetime import datetime, timedelta
import random
from pathlib import Path

HOSTNAME = "LabSIM"
USERS = ["admin", "root", "test", "oracle", "guest"]

ATTACK_PROFILES = {
    # 🔴 Muy agresivos
    "192.168.202.97": (60, 120),
    "192.168.202.100": (50, 100),

    # 🟠 Agresivos
    "192.168.202.76": (30, 60),
    "192.168.202.89": (25, 50),
    "192.168.202.93": (20, 45),

    # 🟡 Medios
    "192.168.202.79": (15, 30),
    "192.168.202.85": (10, 25),
    "192.168.202.88": (10, 20),
    "192.168.202.71": (8, 18),

    # 🟢 Bajos / ruido
    "192.168.202.77": (3, 10),
    "192.168.202.80": (3, 10),
    "192.168.202.90": (2, 8),
    "192.168.202.91": (2, 6),
    "192.168.202.92": (1, 5),
    "192.168.202.94": (1, 4),
    "192.168.202.95": (1, 3),
}

# -------------------------
# 1️⃣ Genera líneas (NO TOCAR)
# -------------------------
def generate_simulated_auth_lines():
    lines = []
    now = datetime.now()

    for ip, (min_a, max_a) in ATTACK_PROFILES.items():
        attempts = random.randint(min_a, max_a)

        for _ in range(attempts):
            date = now - timedelta(seconds=random.randint(0, 3600))
            user = random.choice(USERS)

            lines.append(
                f"{date.strftime('%b %d %H:%M:%S')} LabSIM "
                f"authentication failure; logname= uid=0 euid=0 tty=ssh "
                f"ruser= rhost={ip} user={user}"
            )

    return lines


# -------------------------
# 2️⃣ Genera archivo .log
# -------------------------
def generate_simulated_log_file():
    base_dir = Path("data/uploads") 
    base_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = base_dir / f"simulated_auth_{timestamp}.log"

    lines = generate_simulated_auth_lines()

    with open(file_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

    return str(file_path)
