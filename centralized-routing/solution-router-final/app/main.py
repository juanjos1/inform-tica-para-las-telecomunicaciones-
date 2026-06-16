"""
Router application entry point (NFR-03).

Usage:
    python -m app.main --id R1 --ip 127.0.0.1 --port 5001 \
                       --ctrl-host 127.0.0.1 --ctrl-port 9000 [--protocol tcp|udp]
"""
import argparse
import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.controllers.router_app_controller import RouterAppController
from app.network.notification_server import NotificationServer
from app.views.router_cli_view import show_router_info
from app.views.routing_table_view import show_routing_table
from app.views.neighbor_view import show_neighbors
from app.views.forwarding_view import show_forwarding
from app.utils.constants import MSG_LINK_COST
from app.utils.logger import logger


def interactive_menu(app: RouterAppController):
    """CLI menu for the router (NFR-03, NFR-04, FR-07)."""
    while True:
        print("\n[Router Menu]")
        print("  1. Register with controller")
        print("  2. Add neighbor")
        print("  3. Remove neighbor")          # Fix #3
        print("  4. Send topology to controller")
        print("  5. Show routing table (show routing-table)")
        print("  6. Show neighbors")
        print("  7. Simulate link cost change")
        print("  8. Forward to destination (simulate)")
        print("  9. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            ok = app.registration_ctrl.register(
                app.router.router_id, app.router.ip, app.router.port
            )
            print("Registered!" if ok else "Registration failed.")

        elif choice == "2":
            nid  = input("  Neighbor ID: ").strip()
            cost = float(input("  Link cost: ").strip())
            # Fix #7 & #8: add_neighbor now returns (ok, msg)
            ok, msg = app.neighbor_ctrl.add_neighbor(nid, cost)
            print(f"  {'OK' if ok else 'ERROR'}: {msg}")

        elif choice == "3":
            # Fix #3: explicit neighbor removal
            nid = input("  Neighbor ID to remove: ").strip()
            ok, msg = app.neighbor_ctrl.remove_neighbor(nid)
            print(f"  {'OK' if ok else 'ERROR'}: {msg}")
            if ok:
                print("  Tip: send topology to controller (option 4) so routes are recalculated.")

        elif choice == "4":
            response = app.neighbor_ctrl.send_to_controller(app.router.router_id)
            if response.get("type") == "ROUTING_TABLE":
                entries = response.get("routing_table", [])
                app.routing_table_ctrl.receive_routing_table(entries)
                print("Topology sent and routing table received.")
            else:
                print(f"Response: {response}")

        elif choice == "5":
            show_routing_table(app.routing_table_ctrl.get_table())

        elif choice == "6":
            show_neighbors(app.neighbor_ctrl.service.neighbors)

        elif choice == "7":
            dest = input("  Destination router ID: ").strip()

            # Fix #9: verify destination is a known neighbor before sending.
            known_ids = [n.neighbor_id for n in app.neighbor_ctrl.service.neighbors]
            if dest not in known_ids:
                print(f"  ERROR: '{dest}' is not a neighbor of {app.router.router_id}. "
                      f"No link cost update sent.")
                print(f"  Current neighbors: {known_ids if known_ids else '(none)'}")
            else:
                cost = float(input("  New cost: ").strip())

                # Fix: update the cost in the local neighbors list so that a
                # subsequent "Send topology to controller" (option 4) sends
                # the updated cost instead of the original stale one.
                ok, upd_msg = app.neighbor_ctrl.service.update_neighbor_cost(dest, cost)
                if not ok:
                    print(f"  WARNING: could not update local neighbor cost: {upd_msg}")

                msg = {
                    "type": MSG_LINK_COST,
                    "source": app.router.router_id,
                    "destination": dest,
                    "cost": cost,
                }
                conn = app.neighbor_ctrl.service.connection
                resp = conn.send(msg)
                print(f"Link cost update response: {resp.get('type')} - {resp.get('info', '')}")

        elif choice == "8":
            dest = input("  Destination: ").strip()
            next_hop = app.forwarding_ctrl.forward(dest)
            show_forwarding(dest, next_hop)

        elif choice == "9":
            logger.info("Router shutting down.")
            sys.exit(0)
        else:
            print("Invalid option.")


def main():
    parser = argparse.ArgumentParser(description="Centralized Routing Router Application")
    parser.add_argument("--id",        required=True, help="Router ID (e.g. R1)")
    parser.add_argument("--ip",        default="127.0.0.1", help="This router's IP")
    parser.add_argument("--port",      type=int, required=True, help="This router's port")
    parser.add_argument("--ctrl-host", default="127.0.0.1", help="Controller host")
    parser.add_argument("--ctrl-port", type=int, default=9000, help="Controller port")
    parser.add_argument("--protocol",  choices=["tcp", "udp"], default="tcp")
    args = parser.parse_args()

    app = RouterAppController(
        router_id=args.id,
        ip=args.ip,
        port=args.port,
        controller_host=args.ctrl_host,
        controller_port=args.ctrl_port,
        protocol=args.protocol,
    )

    # --- Fix #6: start the notification server so the controller can push
    #             routing table updates to this router (bidirectional neighbor
    #             notification).  The server binds to the same IP and port that
    #             this router advertised during registration so the controller
    #             knows where to reach it via client_handler.send_routing_table().
    notification_srv = NotificationServer(
        host=args.ip,
        port=args.port,
        on_routing_table=app.routing_table_ctrl.receive_routing_table,
    )
    srv_thread = threading.Thread(target=notification_srv.start, daemon=True)
    srv_thread.start()
    logger.info(
        f"NotificationServer started on {args.ip}:{args.port} "
        f"(listening for controller push notifications)"
    )
    # --- End Fix #6 ---

    show_router_info(app.router)
    interactive_menu(app)


if __name__ == "__main__":
    main()
