"""Link model: directed link between two routers."""


class Link:
    def __init__(self, source: str, destination: str, cost: float):
        self.source = source
        self.destination = destination
        self.cost = cost

    def to_dict(self) -> dict:
        return {"source": self.source, "destination": self.destination, "cost": self.cost}
