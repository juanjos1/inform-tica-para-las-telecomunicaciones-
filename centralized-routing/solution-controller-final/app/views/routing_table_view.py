"""CLI view: display routing tables (FR-07)."""


def show_routing_table(router_id: str, entries: list):
    print(f"\n=== Routing Table for {router_id} ===")
    print(f"  {'Destination':<15} {'Next Hop':<15} {'Cost':<10}")
    print("  " + "-" * 40)
    for e in entries:
        cost = e['cost'] if isinstance(e, dict) else e.cost
        dest = e['destination'] if isinstance(e, dict) else e.destination
        hop = e['next_hop'] if isinstance(e, dict) else e.next_hop
        print(f"  {dest:<15} {hop:<15} {cost:<10}")
    print()


def show_all_routing_tables(tables: dict):
    for router_id, table in tables.items():
        show_routing_table(router_id, table.entries)
