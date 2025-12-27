import re
from collections import Counter

LOG_FILE = "../data/Linux_2k.log"

# Regex
IP_REGEX = re.compile(r"rhost=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")
DATE_REGEX = re.compile(
    r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d+:\d+:\d+"
)
USER_REGEX = re.compile(r"user=([a-zA-Z0-9_-]+)")

ip_counter = Counter()
user_counter = Counter()
date_counter = Counter()

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "authentication failure" in line or "Failed password" in line:

            # IP
            ip_match = IP_REGEX.search(line)
            if ip_match:
                ip_counter[ip_match.group(1)] += 1

            # Fecha
            date_match = DATE_REGEX.search(line)
            if date_match:
                date_counter[date_match.group()] += 1

            # Usuario
            user_match = USER_REGEX.search(line)
            if user_match:
                user_counter[user_match.group(1)] += 1
            else:
                user_counter["unknown"] += 1

# Resultados
print("\n🔐 IPs más agresivas:")
for ip, count in ip_counter.most_common(5):
    print(f"{ip} -> {count}")

print("\n👤 Usuarios más atacados:")
for user, count in user_counter.most_common(5):
    print(f"{user} -> {count}")

print("\n🕒 Momentos con más intentos:")
for date, count in date_counter.most_common(5):
    print(f"{date} -> {count}")


def classify_attack(count):
    if count < 5:
        return "BAJO"
    elif count <= 20:
        return "MEDIO"
    else:
        return "ALTO"

print("\n🚨 Clasificación de ataques por IP:\n")

for ip, count in ip_counter.most_common(10):
    level = classify_attack(count)
    print(f"{ip} -> {count} intentos | Nivel: {level}")
