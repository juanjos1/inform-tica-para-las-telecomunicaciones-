"""Forwarding decision controller."""
from app.services.forwarding_service import ForwardingService


class ForwardingController:
    def __init__(self, service: ForwardingService):
        self.service = service

    def forward(self, destination: str) -> str:
        return self.service.get_next_hop(destination)
