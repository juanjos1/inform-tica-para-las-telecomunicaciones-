"""Neighbor model."""


class Neighbor:
    def __init__(self, neighbor_id: str, cost: float):
        self.neighbor_id = neighbor_id
        self.cost = cost

    def to_dict(self) -> dict:
        return {"neighbor_id": self.neighbor_id, "cost": self.cost}
