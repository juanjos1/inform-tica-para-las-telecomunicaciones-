"""JSON helpers (NFR-04)."""
import json


def encode_message(data: dict) -> bytes:
    """Serialize dict → UTF-8 JSON bytes."""
    return json.dumps(data).encode("utf-8")


def decode_message(raw: bytes) -> dict:
    """Deserialize UTF-8 JSON bytes → dict. Raises ValueError on bad JSON."""
    return json.loads(raw.decode("utf-8"))
