"""Data access: persist routing tables."""
import json, os

_PATH = os.path.join(os.path.dirname(__file__), "../data/routing_tables.json")


def save_routing_tables(tables: dict):
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    with open(_PATH, "w") as f:
        json.dump({k: v.to_dict() for k, v in tables.items()}, f, indent=2)
