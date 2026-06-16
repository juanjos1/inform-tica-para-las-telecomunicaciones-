"""Build outgoing messages."""
from app.utils.constants import MSG_ACK


def ack_message(info: str = "OK") -> dict:
    return {"type": MSG_ACK, "info": info}
