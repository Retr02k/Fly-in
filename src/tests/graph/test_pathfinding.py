from fly_in.graph.pathfinding import GraphTraversal
from fly_in.model.hub import Hub
from fly_in.model.map import Map


def make_traversal() -> GraphTraversal:
    hubs = {
        name: Hub(name=name)
        for name in ("start", "junction", "path_a", "path_b", "goal")
    }
    drone_map = Map(
        nb_drones=1,
        hubs=hubs,
        connections=[],
        start_hub="start",
        end_hub="goal",
    )
    return GraphTraversal(drone_map)


def test_bfs_returns_a_shortest_path() -> None:
    connections: dict[str, dict[str, int]] = {
        "start": {"junction": 1},
        "junction": {"start": 1, "path_a": 1, "path_b": 1},
        "path_a": {"junction": 1, "goal": 1},
        "path_b": {"junction": 1, "goal": 1},
        "goal": {"path_a": 1, "path_b": 1},
    }

    path = make_traversal().bfs(connections, "start", "goal")

    assert path in (
        ["start", "junction", "path_a", "goal"],
        ["start", "junction", "path_b", "goal"],
    )


def test_bfs_handles_cycles() -> None:
    connections: dict[str, dict[str, int]] = {
        "start": {"loop": 1},
        "loop": {"start": 1, "goal": 1},
        "goal": {"loop": 1},
    }

    assert make_traversal().bfs(connections, "start", "goal") == [
        "start",
        "loop",
        "goal",
    ]


def test_bfs_returns_none_when_goal_is_unreachable() -> None:
    connections: dict[str, dict[str, int]] = {
        "start": {"junction": 1},
        "junction": {"start": 1},
        "goal": {},
    }

    assert make_traversal().bfs(connections, "start", "goal") is None


def test_bfs_returns_start_when_start_is_goal() -> None:
    connections: dict[str, dict[str, int]] = {"start": {}}

    assert make_traversal().bfs(connections, "start", "start") == ["start"]
