"""Registration controller (FR-01)."""
from app.services.registration_service import RegistrationService


class RegistrationController:
    def __init__(self, service: RegistrationService):
        self.service = service

    def register(self, router_id: str, ip: str, port: int) -> bool:
        return self.service.register(router_id, ip, port)
