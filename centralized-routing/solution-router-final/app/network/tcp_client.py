"""TCP client: send a message to the controller and receive the response."""
import socket
from app.utils.constants import BUFFER_SIZE
from app.utils.json_utils import encode_message, decode_message
from app.utils.logger import logger


def send_and_receive(host: str, port: int, message: dict) -> dict:
    """Send JSON message to controller, return parsed response."""
    try:
        with socket.create_connection((host, port), timeout=10) as s:
            s.sendall(encode_message(message))
            raw = b""
            while True:
                chunk = s.recv(BUFFER_SIZE)
                if not chunk:
                    break
                raw += chunk
                if len(chunk) < BUFFER_SIZE:
                    break
            return decode_message(raw)
    except Exception as e:
        logger.error(f"TCP error contacting {host}:{port}: {e}")
        return {"type": "ERROR", "reason": str(e)}
