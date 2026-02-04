# tools/generate_simulated_auth_log.py

import random
from datetime import datetime, timedelta

HOSTNAME = "LabSIM"
USERS = ["admin", "root", "test", "oracle", "guest"]
IPS = [
    "192.168.202.79",
    "192.168.202.76",
    "192.168.202.100",
    "192.168.202.89",
    "192.168.202.97",
    "192.168.202.93"
]

def random_date(start, end):
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)

def auth_block(date, pid, user, ip, port):
    ts = date.strftime('%b %d %H:%M:%S')
    return [
        f"{ts} {HOSTNAME} sshd[{pid}]: Invalid user {user} from {ip}",
        f"{ts} {HOSTNAME} sshd[{pid}]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip}",
        f"{ts} {HOSTNAME} sshd[{pid}]: Failed password for invalid user {user} from {ip} port {port} ssh2",
        f"{ts} {HOSTNAME} sshd[{pid}]: Connection closed by {ip} [preauth]",
    ]

def generate_log(
    output_file="data/simulated/simulated_auth.log",
    min_attempts=5,
    max_attempts=120
):
    start_date = datetime.now() - timedelta(hours=2)
    end_date = datetime.now()

    lines = []

    for ip in IPS:
        attempts = random.randint(min_attempts, max_attempts)
        for _ in range(attempts):
            date = random_date(start_date, end_date)
            pid = random.randint(3000, 5000)
            user = random.choice(USERS)
            port = random.randint(1024, 65535)
            lines.extend(auth_block(date, pid, user, ip, port))

    # Orden cronológico
    lines.sort()

    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + "\n")

    print(f"[OK] Log simulado generado: {output_file}")
    print(f"[INFO] Líneas generadas: {len(lines)}")

if __name__ == "__main__":
    generate_log()
