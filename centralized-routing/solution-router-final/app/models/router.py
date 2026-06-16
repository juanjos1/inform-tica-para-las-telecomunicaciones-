"""Local router model."""


class Router:
    def __init__(self, router_id: str, ip: str, port: int):
        self.router_id = router_id
        self.ip = ip
        self.port = port

    def to_dict(self) -> dict:
        return {"router_id": self.router_id, "ip": self.ip, "port": self.port}
