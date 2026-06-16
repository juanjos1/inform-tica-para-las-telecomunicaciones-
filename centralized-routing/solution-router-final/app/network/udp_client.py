"""UDP client alternative."""
import socket
from app.utils.constants import BUFFER_SIZE
from app.utils.json_utils import encode_message, decode_message
from app.utils.logger import logger


def send_and_receive(host: str, port: int, message: dict) -> dict:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            s.sendto(encode_message(message), (host, port))
            raw, _ = s.recvfrom(BUFFER_SIZE)
            return decode_message(raw)
    except Exception as e:
        logger.error(f"UDP error contacting {host}:{port}: {e}")
        return {"type": "ERROR", "reason": str(e)}
