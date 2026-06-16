"""Dijkstra shortest-path service (FR-04)."""
import heapq
from typing import Dict, List, Tuple
from app.models.topology import Topology


def dijkstra(topology: Topology, source: str) -> Dict[str, Tuple[float, List[str]]]:
    """
    Compute shortest paths from source to all other nodes.

    Returns:
        dict  router_id -> (cost, path_list)
    """
    nodes = topology.get_nodes()
    dist = {n: float("inf") for n in nodes}
    prev = {n: None for n in nodes}
    dist[source] = 0.0

    heap = [(0.0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for v, weight in topology.get_neighbors(u):
            alt = dist[u] + weight
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    # Reconstruct paths
    result = {}
    for node in nodes:
        if node == source:
            continue
        path = []
        current = node
        while current is not None:
            path.insert(0, current)
            current = prev[current]
        if path and path[0] == source:
            result[node] = (dist[node], path)

    return result
