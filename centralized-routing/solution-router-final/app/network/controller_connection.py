"""Facade that selects TCP or UDP based on configuration."""
from app.network import tcp_client, udp_client


class ControllerConnection:
    def __init__(self, host: str, port: int, protocol: str = "tcp"):
        self.host = host
        self.port = port
        self.protocol = protocol.lower()

    def send(self, message: dict) -> dict:
        if self.protocol == "udp":
            return udp_client.send_and_receive(self.host, self.port, message)
        return tcp_client.send_and_receive(self.host, self.port, message)
