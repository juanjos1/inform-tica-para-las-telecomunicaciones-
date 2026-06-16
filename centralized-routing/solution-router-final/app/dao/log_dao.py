"""Append log events (FR-09)."""
import json, os
from datetime import datetime

_PATH = os.path.join(os.path.dirname(__file__), "../data/logs.json")


def append_log(event: str, detail: dict = None):
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    entry = {"timestamp": datetime.now().isoformat(), "event": event, "detail": detail or {}}
    logs = []
    if os.path.exists(_PATH):
        with open(_PATH) as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with open(_PATH, "w") as f:
        json.dump(logs, f, indent=2)
