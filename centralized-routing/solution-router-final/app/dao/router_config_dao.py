"""Load/save router config."""
import json, os

_PATH = os.path.join(os.path.dirname(__file__), "../config/router_config.json")


def load_config() -> dict:
    if not os.path.exists(_PATH):
        return {}
    with open(_PATH) as f:
        return json.load(f)
