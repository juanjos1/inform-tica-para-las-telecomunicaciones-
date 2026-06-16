"""Utility to proactively send a routing table to a specific router (FR-06)."""
import socket
from app.utils.constants import BUFFER_SIZE, ENCODING
from app.utils.json_utils import encode_message
from app.utils.logger import logger


def send_routing_table(ip: str, port: int, message: dict):
    """Open a TCP connection to a router and deliver its routing table."""
    try:
        with socket.create_connection((ip, port), timeout=5) as s:
            s.sendall(encode_message(message))
            logger.info(f"Routing table sent to {ip}:{port}")
    except Exception as e:
        logger.error(f"Failed to send routing table to {ip}:{port}: {e}")
