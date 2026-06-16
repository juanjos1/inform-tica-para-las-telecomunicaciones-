"""Helpers to build standard JSON messages (NFR-04)."""
from app.utils.constants import MSG_ACK, MSG_ERROR, MSG_ROUTING_TABLE


def ack_message(info: str = "OK") -> dict:
    return {"type": MSG_ACK, "info": info}


def error_message(reason: str) -> dict:
    return {"type": MSG_ERROR, "reason": reason}


def routing_table_message(router_id: str, entries: list) -> dict:
    return {"type": MSG_ROUTING_TABLE, "router_id": router_id, "routing_table": entries}
