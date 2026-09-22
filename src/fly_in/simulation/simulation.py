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

    def _find_route(self, start: str | None = None) -> list[str]:
        route_start = start or self.parsed_map.start_hub
        route = GraphTraversal(self.parsed_map).bfs(
            self.connections,
            route_start,
            self.parsed_map.end_hub,
        )
        if route is None:
            raise ValueError(
                f"No route from {route_start!r} "
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

    def _current_hub_occupancy(self, destination_hub: str) -> bool:
        capacity = self.parsed_map.hubs[destination_hub].max_drones
        occupied = sum(
            drone.status != DroneStatus.DELIVERED
            and drone.current_hub == destination_hub
            for drone in self.drones
        )
        return occupied < capacity

    def _allowed_drones_to_move(self) -> list[tuple[Drone, str]]:
        occupancy = {
            hub_name: sum(
                drone.status != DroneStatus.DELIVERED
                and drone.current_hub == hub_name
                for drone in self.drones
            )
            for hub_name in self.parsed_map.hubs
        }
        link_usage: dict[tuple[str, str], int] = {}
        allowed: list[tuple[Drone, str]] = []

        for drone in sorted(self.drones, key=lambda item: item.drone_id):
            if drone.status == DroneStatus.DELIVERED:
                continue

            route = self._find_route(drone.current_hub)
            if len(route) == 1:
                continue

            next_hub = route[1]
            destination = self.parsed_map.hubs[next_hub]
            link = (drone.current_hub, next_hub)
            link_capacity = self.connections[drone.current_hub][next_hub]

            if occupancy[next_hub] >= destination.max_drones:
                continue
            if link_usage.get(link, 0) >= link_capacity:
                continue

            drone.route = route
            drone.current_route_index = 0
            occupancy[drone.current_hub] -= 1
            occupancy[next_hub] += 1
            link_usage[link] = link_usage.get(link, 0) + 1
            allowed.append((drone, next_hub))

        return allowed

    def step(self) -> list[tuple[int, str, str]]:
        movements: list[tuple[int, str, str]] = []

        allowed_moves = self._allowed_drones_to_move()
        for drone, next_hub in allowed_moves:
            previous_hub = drone.current_hub
            drone.current_route_index += 1
            drone.current_hub = next_hub
            drone.status = (
                DroneStatus.DELIVERED
                if drone.current_hub == self.parsed_map.end_hub
                else DroneStatus.WAITING
            )
            movements.append(
                (drone.drone_id, previous_hub, drone.current_hub)
            )

        if not movements and any(
            drone.status != DroneStatus.DELIVERED for drone in self.drones
        ):
            raise RuntimeError("No drone can move; simulation is deadlocked")

        self.current_turn += 1
        return movements

    def run(self) -> list[list[tuple[int, str, str]]]:
        turns: list[list[tuple[int, str, str]]] = []
        while any(
            drone.status != DroneStatus.DELIVERED for drone in self.drones
        ):
            turns.append(self.step())
        return turns
