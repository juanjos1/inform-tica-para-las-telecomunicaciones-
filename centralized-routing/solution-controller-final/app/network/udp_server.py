"""UDP server alternative (NFR-03)."""
import socket
from app.utils.constants import CONTROLLER_HOST, CONTROLLER_PORT, BUFFER_SIZE
from app.utils.logger import logger


class UDPServer:
    def __init__(self, comm_controller, host=CONTROLLER_HOST, port=CONTROLLER_PORT):
        self.comm_controller = comm_controller
        self.host = host
        self.port = port
        self._running = False

    def start(self):
        self._running = True
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self.host, self.port))
        logger.info(f"UDP server listening on {self.host}:{self.port}")
        while self._running:
            try:
                raw, addr = self._sock.recvfrom(BUFFER_SIZE)
                response = self.comm_controller.handle(raw)
                self._sock.sendto(response, addr)
            except OSError:
                break

    def stop(self):
        self._running = False
        try:
            self._sock.close()
        except Exception:
            pass
