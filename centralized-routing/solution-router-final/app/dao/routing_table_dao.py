"""Persist the local routing table."""
import json, os

_PATH = os.path.join(os.path.dirname(__file__), "../data/routing_table.json")


def save_routing_table(table):
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    with open(_PATH, "w") as f:
        json.dump(table.to_dict(), f, indent=2)
