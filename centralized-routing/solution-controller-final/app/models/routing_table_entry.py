"""Single entry in a routing table."""


class RoutingTableEntry:
    def __init__(self, destination: str, next_hop: str, cost: float):
        self.destination = destination
        self.next_hop = next_hop
        self.cost = cost

    def to_dict(self) -> dict:
        return {"destination": self.destination, "next_hop": self.next_hop, "cost": self.cost}
