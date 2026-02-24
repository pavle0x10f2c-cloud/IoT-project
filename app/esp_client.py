import socket
import os
from urllib import request

HOST = os.getenv("ESP_HOST", "192.168.4.1")  # reads from .env, falls back to default
PORT = int(os.getenv("ESP_PORT", 8888))


def send_data_to_esp(led_value: int) -> None:
    try:
        request.urlopen(f"http://{HOST}", timeout=1)  # ping ESP before sending

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as esp:  # UDP socket
            esp.connect((HOST, PORT))
            esp.send(str(led_value).encode("utf-8"))  # send LED level as bytes
            response = esp.recv(1024).decode("utf-8")
            print(f"[ESP] Response: {response}")

    except Exception:
        print("[ESP] Not available — check connection or .env settings")
