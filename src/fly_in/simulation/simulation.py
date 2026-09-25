from fly_in.graph.builder import GraphBuilder
from fly_in.graph.pathfinding import GraphTraversal
from fly_in.header.header import ZoneType
from fly_in.model.drone import Drone, DroneStatus
from fly_in.model.map import Map
from fly_in.model.movement import PlannedMove
from fly_in.model.transit import TransitState


class Simulator:
    def __init__(self, parsed_map: Map) -> None:
        self.parsed_map = parsed_map
        self.connections = GraphBuilder(parsed_map).connectors_dic()
        self.route = self._find_route()
        self.drones = self._create_drones()
        self.current_turn = 0

    def _find_route(self, start: str | None = None) -> list[str]:
        route_start = start or self.parsed_map.start_hub
        route = GraphTraversal(self.parsed_map).find_best_route(
            self.connections,
            self.parsed_map.hubs,
            route_start,
            self.parsed_map.end_hub,
        )
        if route is None:
            raise ValueError(
                f"No route from {route_start!r} "
                f"to {self.parsed_map.end_hub!r}"
            )
        return route

    @staticmethod
    def _link_key(origin: str, destination: str) -> tuple[str, str]:
        return (
            (origin, destination)
            if origin <= destination
            else (destination, origin)
        )

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

    def _plan_allowed_moves(self) -> list[PlannedMove]:
        occupancy = {
            hub_name: sum(
                drone.status not in (
                    DroneStatus.DELIVERED,
                )
                and drone.current_hub == hub_name
                for drone in self.drones
            )
            for hub_name in self.parsed_map.hubs
        }
        for drone in self.drones:
            if drone.status == DroneStatus.MOVING:
                if drone.transit is None:
                    raise RuntimeError(
                        f"Moving drone {drone.drone_id} has no transit state"
                    )
                occupancy[drone.transit.destination_hub] += 1
        link_usage: dict[tuple[str, str], int] = {}
        for drone in self.drones:
            if drone.status != DroneStatus.MOVING or drone.transit is None:
                continue
            key = self._link_key(
                drone.transit.origin_hub,
                drone.transit.destination_hub,
            )
            link_usage[key] = link_usage.get(key, 0) + 1
        planned: list[PlannedMove] = []

        for drone in sorted(self.drones, key=lambda item: item.drone_id):
            if drone.status != DroneStatus.WAITING:
                continue

            route = self._find_route(drone.current_hub)
            if len(route) == 1:
                continue

            next_hub = route[1]
            destination = self.parsed_map.hubs[next_hub]
            link = (drone.current_hub, next_hub)
            link_key = self._link_key(*link)
            link_capacity = self.connections[drone.current_hub][next_hub]

            if occupancy[next_hub] >= destination.max_drones:
                continue
            if link_usage.get(link_key, 0) >= link_capacity:
                continue

            if destination.zone_type in (
                ZoneType.NORMAL,
                ZoneType.PRIORITY,
            ):
                duration = 1
            elif destination.zone_type == ZoneType.RESTRICTED:
                duration = 2
            else:
                continue

            occupancy[drone.current_hub] -= 1
            occupancy[next_hub] += 1
            link_usage[link_key] = link_usage.get(link_key, 0) + 1
            planned.append(
                PlannedMove(
                    drone=drone,
                    origin_hub=drone.current_hub,
                    destination_hub=next_hub,
                    connection=link,
                    duration=duration,
                )
            )

        return planned

    def _apply_planned_moves(
        self,
        planned_moves: list[PlannedMove],
    ) -> None:
        for move in planned_moves:
            drone = move.drone
            drone.route = self._find_route(move.origin_hub)
            drone.current_route_index = 0
            drone.transit = TransitState(
                origin_hub=move.origin_hub,
                destination_hub=move.destination_hub,
                connection=move.connection,
                remaining_transit_turns=move.duration,
            )
            drone.status = DroneStatus.MOVING

    def _progress_transit(self) -> list[tuple[int, str, str]]:
        movements: list[tuple[int, str, str]] = []

        for drone in self.drones:
            if drone.status != DroneStatus.MOVING:
                continue
            if drone.transit is None:
                raise RuntimeError(
                    f"Moving drone {drone.drone_id} has no transit state"
                )

            drone.transit.remaining_transit_turns -= 1
            if drone.transit.remaining_transit_turns > 0:
                continue

            previous_hub = drone.current_hub
            drone.current_hub = drone.transit.destination_hub
            drone.current_route_index += 1
            drone.status = (
                DroneStatus.DELIVERED
                if drone.current_hub == self.parsed_map.end_hub
                else DroneStatus.WAITING
            )
            drone.transit = None
            movements.append(
                (drone.drone_id, previous_hub, drone.current_hub)
            )

        return movements

    def step(self) -> list[tuple[int, str, str]]:
        movements = self._progress_transit()
        planned_moves = self._plan_allowed_moves()
        self._apply_planned_moves(planned_moves)

        active_transit = any(
            drone.status == DroneStatus.MOVING for drone in self.drones
        )
        if not movements and not planned_moves and not active_transit and any(
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
