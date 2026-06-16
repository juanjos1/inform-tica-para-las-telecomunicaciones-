"""TCP server that listens for router connections (NFR-03)."""
import socket
import threading
from app.utils.constants import CONTROLLER_HOST, CONTROLLER_PORT, BUFFER_SIZE
from app.utils.logger import logger


class TCPServer:
    def __init__(self, comm_controller, host=CONTROLLER_HOST, port=CONTROLLER_PORT):
        self.comm_controller = comm_controller
        self.host = host
        self.port = port
        self._running = False

    def start(self):
        self._running = True
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(10)
        logger.info(f"TCP server listening on {self.host}:{self.port}")
        while self._running:
            try:
                conn, addr = self._server_socket.accept()
                t = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
                t.start()
            except OSError:
                break

    def _handle_client(self, conn: socket.socket, addr):
        logger.info(f"Connection from {addr}")
        try:
            raw = b""
            while True:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                raw += chunk
                if len(chunk) < BUFFER_SIZE:
                    break
            if raw:
                response = self.comm_controller.handle(raw)
                conn.sendall(response)
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            conn.close()

    def stop(self):
        self._running = False
        try:
            self._server_socket.close()
        except Exception:
            pass
