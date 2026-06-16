"""Display forwarding decision."""


def show_forwarding(destination: str, next_hop: str):
    if next_hop:
        print(f"  Forward to '{destination}' via next hop: {next_hop}")
    else:
        print(f"  No route to '{destination}'")
