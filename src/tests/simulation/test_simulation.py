from fly_in.parser.map_parser import MapParser
from fly_in.simulation.simulation import Simulator


def test_simulator_creates_one_drone_per_map_count() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()

    simulator = Simulator(drone_map)

    assert len(simulator.drones) == drone_map.nb_drones
    assert all(
        drone.current_hub == drone_map.start_hub
        for drone in simulator.drones
    )
    assert all(
        drone.route == ["start", "waypoint1", "waypoint2", "goal"]
        for drone in simulator.drones
    )


def test_simulator_moves_all_drones_to_goal() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()

    simulator = Simulator(drone_map)
    turns = simulator.run()

    assert len(turns) == 4
    assert simulator.current_turn == 4
    assert all(
        drone.current_hub == drone_map.end_hub
        for drone in simulator.drones
    )


def test_simulator_respects_hub_capacity() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/03_basic_capacity.txt"
    ).parse()

    simulator = Simulator(drone_map)
    simulator.step()

    assert sum(
        drone.current_hub == "bottleneck"
        for drone in simulator.drones
    ) == 2


def test_normal_moves_arrive_during_their_turn() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()

    simulator = Simulator(drone_map)
    arrivals = simulator.step()

    assert arrivals == [(1, "start", "waypoint1")]
    assert simulator.drones[0].current_hub == "waypoint1"
    assert simulator.drones[0].transit is None


def test_restricted_arrival_frees_connection_before_new_planning() -> None:
    drone_map = MapParser(
        filepath="src/maps/test_edge_cases.txt"
    ).parse()

    simulator = Simulator(drone_map)
    simulator.step()
    arrivals = simulator.step()

    assert (1, "start", "gate") in arrivals
    assert simulator.drones[1].transit is not None
    assert simulator.drones[1].transit.destination_hub == "gate"


def test_simulator_respects_link_capacity() -> None:
    drone_map = MapParser(
        filepath="src/maps/medium/03_priority_puzzle.txt"
    ).parse()

    simulator = Simulator(drone_map)
    simulator.step()
    simulator.step()
    third_turn = simulator.step()

    assert sum(
        destination == "goal"
        for _, _, destination in third_turn
    ) <= 2


def test_simulator_treats_end_hub_as_unlimited_sink() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/03_basic_capacity.txt"
    ).parse()

    simulator = Simulator(drone_map)

    assert len(simulator.run()) <= 6
    assert all(
        drone.current_hub == drone_map.end_hub
        for drone in simulator.drones
    )


def test_circular_loop_preserves_restricted_link_capacity() -> None:
    drone_map = MapParser(
        filepath="src/maps/medium/02_circular_loop.txt"
    ).parse()

    simulator = Simulator(drone_map)
    restricted_departures: list[int] = []

    while any(drone.status.value != "delivered" for drone in simulator.drones):
        simulator.step()
        restricted_departures.extend(
            simulator.current_turn
            for move in simulator.last_planned_moves
            if move.destination_hub == "exit_point"
        )

    # Two normal moves are required before the first departure. The
    # capacity-one restricted link remains occupied for two turns.
    assert restricted_departures == [3, 4, 5, 6, 7, 8]
    assert simulator.current_turn == 9


def test_edge_case_map_waits_until_capacity_is_available() -> None:
    drone_map = MapParser(
        filepath="src/maps/test_edge_cases.txt"
    ).parse()

    simulator = Simulator(drone_map)

    assert len(simulator.run()) == 5
    assert all(
        drone.current_hub == drone_map.end_hub
        for drone in simulator.drones
    )
