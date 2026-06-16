"""Persist neighbor information."""
import json, os
from app.models.neighbor import Neighbor

_PATH = os.path.join(os.path.dirname(__file__), "../data/neighbors.json")


def save_neighbors(neighbors: list):
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    with open(_PATH, "w") as f:
        json.dump([n.to_dict() for n in neighbors], f, indent=2)


def load_neighbors() -> list:
    if not os.path.exists(_PATH):
        return []
    with open(_PATH) as f:
        data = json.load(f)
    return [Neighbor(n["neighbor_id"], n["cost"]) for n in data]
