"""JSON helpers (NFR-04)."""
import json


def encode_message(data: dict) -> bytes:
    return json.dumps(data).encode("utf-8")


def decode_message(raw: bytes) -> dict:
    return json.loads(raw.decode("utf-8"))
