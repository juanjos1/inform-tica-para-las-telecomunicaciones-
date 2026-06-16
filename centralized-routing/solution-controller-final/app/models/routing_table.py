"""Routing table for a single router."""
from typing import List
from app.models.routing_table_entry import RoutingTableEntry


class RoutingTable:
    def __init__(self, router_id: str):
        self.router_id = router_id
        self.entries: List[RoutingTableEntry] = []

    def add_entry(self, entry: RoutingTableEntry):
        self.entries.append(entry)

    def to_dict(self) -> dict:
        return {"router_id": self.router_id, "entries": [e.to_dict() for e in self.entries]}
