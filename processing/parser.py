import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOG_PATH = BASE_DIR / "data" / "Linux_2k.log"

LOG_PATTERN = re.compile(
    r'^(?P<date>\w+\s+\d+\s[\d:]+).*authentication failure.*rhost=(?P<rhost>[^\s]+)(?:.*user=(?P<user>\w+))?'
)

def parse_log(log_path=None):
    """
    Parsea un archivo de log.
    Si no se indica ruta, usa el log por defecto.
    """
    if log_path is None:
        log_path = DEFAULT_LOG_PATH

    results = []

    total_lines = 0
    parsed_lines = 0
    discarded_lines = 0

    with open(log_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            total_lines += 1

            match = LOG_PATTERN.search(line)
            if match:
                data = match.groupdict()
                if not data.get("user"):
                    data["user"] = "unknown"

                results.append(data)
                parsed_lines += 1
            else:
                discarded_lines += 1

    return results, {
        "total_lines": total_lines,
        "parsed_lines": parsed_lines,
        "discarded_lines": discarded_lines,
    }


if __name__ == "__main__":
    results, stats = parse_log()

    print(f"Líneas totales: {stats['total_lines']}")
    print(f"Líneas analizadas: {stats['parsed_lines']}")
    print(f"Líneas descartadas: {stats['discarded_lines']}")
    print(f"Registros detectados: {len(results)}")
    print(results[:5])

