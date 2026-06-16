"""
Controller application entry point (NFR-03).

Usage:
    python -m app.main [--protocol tcp|udp] [--host HOST] [--port PORT]
"""
import argparse
import threading
import sys
import os

# Allow running from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.controllers.controller_app_controller import ControllerAppController
from app.network.tcp_server import TCPServer
from app.network.udp_server import UDPServer
from app.views.controller_cli_view import show_registered_routers
from app.views.topology_view import show_topology
from app.views.routing_table_view import show_all_routing_tables
from app.views.log_view import show_recent_logs
from app.utils.logger import logger


def interactive_menu(app_ctrl: ControllerAppController):
    """Simple CLI menu for manual inspection (NFR-04)."""
    while True:
        print("\n[Controller Menu]")
        print("  1. Show registered routers")
        print("  2. Show topology")
        print("  3. Show routing tables")
        print("  4. Show recent logs")
        print("  5. Remove router")
        print("  6. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            show_registered_routers(app_ctrl.registry.all_routers())
        elif choice == "2":
            show_topology(app_ctrl.topology_ctrl.topology)
        elif choice == "3":
            show_all_routing_tables(app_ctrl.routing_ctrl.routing_tables)
        elif choice == "4":
            show_recent_logs()
        elif choice == "5":
            router_id = input("  Router ID to remove: ").strip()
            if not router_id:
                print("  [!] No router ID entered.")
            elif app_ctrl.remove_router(router_id):
                print(f"  [OK] Router '{router_id}' removed. Routing tables recomputed.")
            else:
                print(f"  [!] Router '{router_id}' not found in registry.")
        elif choice == "6":
            logger.info("Controller shutting down.")
            sys.exit(0)
        else:
            print("Invalid option.")


def main():
    parser = argparse.ArgumentParser(description="Centralized Routing Controller")
    parser.add_argument("--protocol", choices=["tcp", "udp"], default="tcp")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    app_ctrl = ControllerAppController()
    comm_ctrl = app_ctrl.get_comm_controller()

    if args.protocol == "tcp":
        server = TCPServer(comm_ctrl, host=args.host, port=args.port)
    else:
        server = UDPServer(comm_ctrl, host=args.host, port=args.port)

    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    logger.info(f"Server started [{args.protocol.upper()}] on {args.host}:{args.port}")

    interactive_menu(app_ctrl)


if __name__ == "__main__":
    main()
