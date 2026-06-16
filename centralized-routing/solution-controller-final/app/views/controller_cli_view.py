"""CLI view: display controller status information (NFR-04)."""


def show_registered_routers(routers: list):
    print("\n=== Registered Routers ===")
    if not routers:
        print("  (none)")
    for r in routers:
        print(f"  {r.router_id:10s} | {r.ip}:{r.port} | {r.status}")
    print()


def show_topology(topology_dict: dict):
    print("\n=== Network Topology ===")
    if not topology_dict:
        print("  (empty)")
    for node, neighbors in topology_dict.items():
        for n in neighbors:
            print(f"  {node} --[{n['cost']}]--> {n['neighbor']}")
    print()
