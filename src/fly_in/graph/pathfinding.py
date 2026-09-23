import heapq
from fly_in.header.header import ZoneType
from fly_in.model.hub import Hub
from fly_in.model.map import Map


ZONE_COST = {
    ZoneType.NORMAL: 1,
    ZoneType.PRIORITY: 1,
    ZoneType.RESTRICTED: 2,
}


class GraphTraversal:
    def __init__(self, drone_map: Map) -> None:
        self.drone_map = drone_map

    def find_best_route(
        self,
        connections: dict[str, dict[str, int]],
        hubs: dict[str, Hub],
        start: str,
        goal: str,
    ) -> list[str] | None:
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
        path: list[str] = []
        current: str | None = goal

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        return path
