from fly_in.graph.builder import GraphBuilder
from fly_in.graph.pathfinding import GraphTraversal
from fly_in.model.drone import Drone, DroneStatus
from fly_in.model.map import Map


class Simulator:
    def __init__(self, parsed_map: Map) -> None:
        self.parsed_map = parsed_map
        self.connections = GraphBuilder(parsed_map).connectors_dic()
        self.route = self._find_route()
        self.drones = self._create_drones()
        self.current_turn = 0

    def _find_route(self) -> list[str]:
        route = GraphTraversal(self.parsed_map).bfs(
            self.connections,
            self.parsed_map.start_hub,
            self.parsed_map.end_hub,
        )
        if route is None:
            raise ValueError(
                f"No route from {self.parsed_map.start_hub!r} "
                f"to {self.parsed_map.end_hub!r}"
            )
        return route

    def _create_drones(self) -> list[Drone]:
        return [
            Drone(
                drone_id=drone_id,
                current_hub=self.route[0],
                route=self.route.copy(),
                status=(
                    DroneStatus.DELIVERED
                    if len(self.route) == 1
                    else DroneStatus.WAITING
                ),
            )
            for drone_id in range(1, self.parsed_map.nb_drones + 1)
        ]

    def step(self) -> list[tuple[int, str, str]]:
        movements: list[tuple[int, str, str]] = []

        for drone in self.drones:
            if drone.status == DroneStatus.DELIVERED:
                continue

            previous_hub = drone.current_hub
            drone.current_route_index += 1
            drone.current_hub = drone.route[drone.current_route_index]
            drone.status = (
                DroneStatus.DELIVERED
                if drone.current_hub == self.parsed_map.end_hub
                else DroneStatus.WAITING
            )
            movements.append(
                (drone.drone_id, previous_hub, drone.current_hub)
            )

        self.current_turn += 1
        return movements

    def run(self) -> list[list[tuple[int, str, str]]]:
        turns: list[list[tuple[int, str, str]]] = []
        while any(
            drone.status != DroneStatus.DELIVERED for drone in self.drones
        ):
            turns.append(self.step())
        return turns
