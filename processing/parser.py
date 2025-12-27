import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = BASE_DIR / "data" / "Linux_2k.log"

LOG_PATTERN = re.compile(
    r'^(?P<date>\w+\s+\d+\s[\d:]+).*authentication failure.*rhost=(?P<rhost>[^\s]+)(?:.*user=(?P<user>\w+))?'
)

def parse_log(log_path=LOG_PATH):
    results = []

    with open(log_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = LOG_PATTERN.search(line)
            if match:
                data = match.groupdict()
                if not data.get("user"):
                    data["user"] = "unknown"
                results.append(data)

    return results


if __name__ == "__main__":
    data = parse_log()
    print(f"Registros detectados: {len(data)}")
    print(data[:5])
