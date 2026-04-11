import errno
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request


def _addr_in_use(exc: OSError) -> bool:
    if exc.errno == errno.EADDRINUSE:
        return True
    # Windows
    if getattr(exc, "winerror", None) == 10048:
        return True
    return False


def _port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError as exc:
            if _addr_in_use(exc):
                return False
            raise


def _existing_calmiq_server(port: int) -> bool:
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/", timeout=3
        ) as resp:
            body = json.loads(resp.read().decode())
        return isinstance(body, dict) and "message" in body
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return False


if __name__ == "__main__":
    os.environ.setdefault("PORT", "7860")
    port = int(os.getenv("PORT", "7860"))
    host = "0.0.0.0"

    try:
        if not _port_available(host, port):
            # Another process may still be binding; wait for our own / root payload.
            for _ in range(40):
                if _existing_calmiq_server(port):
                    print(
                        f"Port {port} already serves this API; "
                        "skipping a second uvicorn bind.",
                        flush=True,
                    )
                    raise SystemExit(0)
                time.sleep(0.15)

            print(
                f"Port {port} is in use and does not look like this API; "
                "set PORT to a free port or stop the conflicting process.",
                flush=True,
            )
            raise SystemExit(1)

        from server.app import main

        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"inference.py failed: {exc}", flush=True)
        raise

