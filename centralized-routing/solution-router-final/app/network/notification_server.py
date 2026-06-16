"""
Lightweight TCP server that receives push notifications from the controller.

This component allows the controller to proactively deliver updated routing
tables to this router (Fix #6: bidirectional neighbor notification).

Architecture note: the router remains a *client* of the controller for all
outgoing messages (registration, topology updates, link-cost changes).  This
server only handles *incoming* pushes and therefore does not change the
overall client/server roles in the system.
"""
import socket
import threading
from app.utils.constants import BUFFER_SIZE
from app.utils.json_utils import decode_message, encode_message
from app.services.message_service import ack_message
from app.utils.logger import logger


class NotificationServer:
    """
    Listens on the router's own IP:port for messages pushed by the controller.

    Accepted message types
    ----------------------
    ROUTING_TABLE   – controller delivers an updated routing table.
                      The server calls on_routing_table(entries) so the
                      RoutingTableController can persist the new table.

    Any other type is acknowledged with ACK and logged as a warning.
    """

    def __init__(self, host: str, port: int, on_routing_table):
        """
        Parameters
        ----------
        host              : IP address to bind to (same as router's --ip).
        port              : TCP port to bind to (same as router's --port).
        on_routing_table  : callable(entries: list) – invoked when a
                            ROUTING_TABLE push arrives so the router can
                            update its internal state.
        """
        self.host = host
        self.port = port
        self.on_routing_table = on_routing_table
        self._running = False
        self._server_socket = None

    def start(self):
        """Bind and accept connections in a blocking loop (run in a daemon thread)."""
        self._running = True
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(10)
        logger.info(f"NotificationServer listening on {self.host}:{self.port}")
        while self._running:
            try:
                conn, addr = self._server_socket.accept()
                t = threading.Thread(
                    target=self._handle, args=(conn, addr), daemon=True
                )
                t.start()
            except OSError:
                break

    def _handle(self, conn: socket.socket, addr):
        logger.info(f"NotificationServer: connection from {addr}")
        try:
            raw = b""
            while True:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                raw += chunk
                if len(chunk) < BUFFER_SIZE:
                    break

            if not raw:
                return

            msg = decode_message(raw)
            msg_type = msg.get("type")

            if msg_type == "ROUTING_TABLE":
                entries = msg.get("routing_table", [])
                logger.info(
                    f"NotificationServer: received ROUTING_TABLE push "
                    f"with {len(entries)} entries from controller."
                )
                self.on_routing_table(entries)
                conn.sendall(encode_message(ack_message("ROUTING_TABLE received")))
            else:
                logger.warning(
                    f"NotificationServer: unknown message type '{msg_type}' from {addr}"
                )
                conn.sendall(encode_message(ack_message(f"Unknown type: {msg_type}")))

        except Exception as e:
            logger.error(f"NotificationServer error handling {addr}: {e}")
        finally:
            conn.close()

    def stop(self):
        self._running = False
        try:
            self._server_socket.close()
        except Exception:
            pass
