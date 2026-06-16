"""Router's local routing table (FR-06)."""
from typing import List
from app.models.routing_table_entry import RoutingTableEntry


class RoutingTable:
    def __init__(self, router_id: str):
        self.router_id = router_id
        self.entries: List[RoutingTableEntry] = []

    def update_from_list(self, entries_list: list):
        self.entries = [RoutingTableEntry(e["destination"], e["next_hop"], e["cost"]) for e in entries_list]

    def to_dict(self) -> dict:
        return {"router_id": self.router_id, "entries": [e.to_dict() for e in self.entries]}
