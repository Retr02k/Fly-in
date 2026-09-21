from collections import deque
from fly_in.model.map import Map


class GraphTraversal:
    def __init__(self, drone_map: Map) -> None:
        self.drone_map = drone_map

    def bfs(
        self,
        connections: dict[str, dict[str, int]],
        start: str,
        goal: str,
    ) -> list[str] | None:
        if start not in connections or goal not in connections:
            return None

        visited: set[str] = {start}
        previous: dict[str, str | None] = {start: None}
        queue: deque[str] = deque([start])

        while queue:
            current = queue.popleft()
            if current == goal:
                return self._build_path(previous, goal)

            for neighbor in connections[current]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                previous[neighbor] = current
                queue.append(neighbor)

        return None

    @staticmethod
    def _build_path(
        previous: dict[str, str | None],
        goal: str,) -> list[str]:
        path: list[str] = []
        current: str | None = goal

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        return path
