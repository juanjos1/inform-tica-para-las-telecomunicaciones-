"""Router model: represents a registered router in the network."""


class Router:
    def __init__(self, router_id: str, ip: str, port: int):
        self.router_id = router_id
        self.ip = ip
        self.port = port
        self.status = "active"

    def to_dict(self) -> dict:
        return {"router_id": self.router_id, "ip": self.ip, "port": self.port, "status": self.status}

    def __repr__(self):
        return f"Router(id={self.router_id}, ip={self.ip}, port={self.port})"
