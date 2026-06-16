"""Build routing tables from Dijkstra results (FR-05)."""
from app.models.topology import Topology
from app.models.routing_table import RoutingTable
from app.models.routing_table_entry import RoutingTableEntry
from app.services.dijkstra_service import dijkstra


def build_all_routing_tables(topology: Topology) -> dict:
    """
    Generate a RoutingTable for every node in the topology.

    Returns:
        dict  router_id -> RoutingTable
    """
    tables = {}
    for source in topology.get_nodes():
        paths = dijkstra(topology, source)
        rt = RoutingTable(source)
        for dest, (cost, path) in paths.items():
            # next hop is the second element of the path (first after source)
            next_hop = path[1] if len(path) > 1 else dest
            rt.add_entry(RoutingTableEntry(dest, next_hop, cost))
        tables[source] = rt
    return tables
