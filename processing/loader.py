import json
from pathlib import Path

DATA_DIR = Path("data")

def load_network_hosts():
    path = DATA_DIR / "network_hosts_summary.json"
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
