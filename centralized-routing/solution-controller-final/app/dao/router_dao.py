"""Data access: persist/load routers from routers.json."""
import json, os
from app.models.router import Router

_PATH = os.path.join(os.path.dirname(__file__), "../data/routers.json")


def save_routers(routers: dict):
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    with open(_PATH, "w") as f:
        json.dump({k: v.to_dict() for k, v in routers.items()}, f, indent=2)


def load_routers() -> dict:
    if not os.path.exists(_PATH):
        return {}
    with open(_PATH) as f:
        data = json.load(f)
    return {k: Router(v["router_id"], v["ip"], v["port"]) for k, v in data.items()}
