"""Display routing table in CLI (FR-07)."""


def show_routing_table(table):
    print(f"\n=== Routing Table for {table.router_id} ===")
    if not table.entries:
        print("  (empty - no routing table received yet)")
        return
    print(f"  {'Destination':<15} {'Next Hop':<15} {'Cost':<10}")
    print("  " + "-" * 40)
    for e in table.entries:
        print(f"  {e.destination:<15} {e.next_hop:<15} {e.cost:<10}")
    print()
