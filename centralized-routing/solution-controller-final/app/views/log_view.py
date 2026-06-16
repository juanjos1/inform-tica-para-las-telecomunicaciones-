"""Log view: print recent log events."""
import json, os

_PATH = os.path.join(os.path.dirname(__file__), "../data/logs.json")


def show_recent_logs(n: int = 20):
    print(f"\n=== Last {n} Log Events ===")
    if not os.path.exists(_PATH):
        print("  (no logs yet)")
        return
    with open(_PATH) as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    for entry in logs[-n:]:
        print(f"  [{entry['timestamp']}] {entry['event']} {entry.get('detail', {})}")
    print()
