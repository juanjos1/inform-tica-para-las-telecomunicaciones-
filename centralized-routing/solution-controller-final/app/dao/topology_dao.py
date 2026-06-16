"""Data access: persist/load topology from topology.json."""
import json, os
from app.models.topology import Topology

_PATH = os.path.join(os.path.dirname(__file__), "../data/topology.json")


def save_topology(topology: Topology):
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    with open(_PATH, "w") as f:
        json.dump(topology.to_dict(), f, indent=2)


def load_topology() -> Topology:
    t = Topology()
    if not os.path.exists(_PATH):
        return t
    with open(_PATH) as f:
        data = json.load(f)
    for node, neighbors in data.items():
        t.add_router(node)
        t.graph[node] = [(n["neighbor"], n["cost"]) for n in neighbors]
    return t
