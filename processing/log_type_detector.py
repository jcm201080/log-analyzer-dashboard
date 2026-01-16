def detect_log_type(log_path, max_lines=20):
    """
    Detecta el tipo de log según su contenido.
    Devuelve: 'auth', 'network' o 'unknown'
    """

    if not log_path:
        return "unknown"

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break

                line = line.lower()

                # 🔐 AUTH logs (Linux / SSH)
                if (
                    "failed password" in line
                    or "accepted password" in line
                    or "authentication failure" in line
                    or "sshd" in line
                ):
                    return "auth"

                # 🌐 NETWORK logs (Zeek conn.log)
                if (
                    "#separator" in line
                    or "#fields" in line
                    or "conn_state" in line
                    or "id.orig_h" in line
                ):
                    return "network"

    except Exception:
        return "unknown"

    return "unknown"
