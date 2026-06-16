"""Display neighbor information."""


def show_neighbors(neighbors: list):
    print("\n=== Neighbors ===")
    if not neighbors:
        print("  (no neighbors configured)")
        return
    for n in neighbors:
        print(f"  {n.neighbor_id}  cost={n.cost}")
    print()
