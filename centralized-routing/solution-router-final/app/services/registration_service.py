"""Handle router registration with the controller (FR-01)."""
from app.network.controller_connection import ControllerConnection
from app.utils.constants import MSG_REGISTER
from app.utils.logger import logger
from app.dao import log_dao


class RegistrationService:
    def __init__(self, connection: ControllerConnection):
        self.connection = connection

    def register(self, router_id: str, ip: str, port: int) -> bool:
        msg = {"type": MSG_REGISTER, "router_id": router_id, "ip": ip, "port": port}
        response = self.connection.send(msg)
        if response.get("type") == "ACK":
            log_dao.append_log("REGISTERED", {"router_id": router_id})
            logger.info(f"Successfully registered as {router_id}")
            return True
        logger.error(f"Registration failed: {response}")
        return False
