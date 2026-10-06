import heapq
from fly_in.model.hub import Hub
from fly_in.model.map import Map
from fly_in.model.zone import ZoneType


ZONE_COST = {
    ZoneType.NORMAL: 1,
    ZoneType.PRIORITY: 1,
    ZoneType.RESTRICTED: 2,
}


class GraphTraversal:
    """Find deterministic weighted routes through a map graph."""

    def __init__(self, drone_map: Map) -> None:
        """Initialize traversal with the map being searched.

        Args:
            drone_map: Map containing zone metadata for route costs.
        """
        self.drone_map = drone_map

    def find_best_route(
        self,
        connections: dict[str, dict[str, int]],
        hubs: dict[str, Hub],
        start: str,
        goal: str,
    ) -> list[str] | None:
        """Find the lowest-cost route, preferring priority zones on ties.

        Args:
            connections: Bidirectional graph adjacency and capacities.
            hubs: Hub metadata used to calculate zone costs.
            start: Name of the route's starting hub.
            goal: Name of the destination hub.

        Returns:
            An ordered list of hub names, or ``None`` if unreachable.
        """
        best_cost: dict[str, int] = {start: 0}
        best_priority_count: dict[str, int] = {start: 0}
        previous: dict[str, str | None] = {start: None}
        priority_queue: list[tuple[int, int, str]] = [(0, 0, start)]

        while priority_queue:
            current_cost, priority_count, current_name = (
                heapq.heappop(priority_queue)
            )
            priority_count = -priority_count

            if (
                current_cost > best_cost[current_name]
                or (
                    current_cost == best_cost[current_name]
                    and priority_count < best_priority_count[current_name]
                )
            ):
                continue

            if current_name == goal:
                return self._build_path(previous, goal)

            for neighbor_name in sorted(connections.get(current_name, {})):
                if neighbor_name not in hubs:
                    continue

                neighbor = hubs[neighbor_name]

                if neighbor.zone_type not in ZONE_COST:
                    continue

                step_cost = ZONE_COST[neighbor.zone_type]
                new_cost = best_cost[current_name] + step_cost
                new_priority_count = best_priority_count[current_name] + (
                        1 if neighbor.zone_type == ZoneType.PRIORITY else 0
                        )

                if neighbor_name not in best_cost:
                    accept = True
                elif new_cost < best_cost[neighbor_name]:
                    accept = True
                elif (
                    new_cost == best_cost[neighbor_name]
                    and new_priority_count
                    > best_priority_count[neighbor_name]
                ):
                    accept = True
                else:
                    accept = False

                if accept:
                    best_cost[neighbor_name] = new_cost
                    best_priority_count[neighbor_name] = new_priority_count
                    previous[neighbor_name] = current_name
                    heapq.heappush(
                        priority_queue,
                        (new_cost, -new_priority_count, neighbor_name),
                    )

        return None

    @staticmethod
    def _build_path(
        previous: dict[str, str | None],
        goal: str,
    ) -> list[str]:
        """Reconstruct a route from predecessor relationships.

        Args:
            previous: Mapping of each visited hub to its predecessor.
            goal: Final hub in the route.

        Returns:
            Hub names ordered from start to goal.
        """
        path: list[str] = []
        current: str | None = goal

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        return path
