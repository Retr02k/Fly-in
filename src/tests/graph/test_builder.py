import pytest

from fly_in.graph.builder import GraphBuilder
from fly_in.model.connection import Connection
from fly_in.model.hub import Hub
from fly_in.model.map import Map


def make_map(connections: list[Connection]) -> Map:
    hubs = {
        "start": Hub(name="start"),
        "junction": Hub(name="junction"),
        "path_a": Hub(name="path_a"),
        "path_b": Hub(name="path_b"),
        "goal": Hub(name="goal"),
    }
    return Map(
        nb_drones=1,
        hubs=hubs,
        connections=connections,
        start_hub="start",
        end_hub="goal",
    )


def test_connectors_dic_keeps_all_bidirectional_neighbors():
    drone_map = make_map(
        [
            Connection(
                from_hub="start",
                to_hub="junction",
                max_link_capacity=2,
            ),
            Connection(from_hub="junction", to_hub="path_a"),
            Connection(from_hub="junction", to_hub="path_b"),
        ]
    )

    connections = GraphBuilder(drone_map).connectors_dic()

    assert connections == {
        "start": {"junction": 2},
        "junction": {"start": 2, "path_a": 1, "path_b": 1},
        "path_a": {"junction": 1},
        "path_b": {"junction": 1},
        "goal": {},
    }


def test_connectors_dic_rejects_unknown_hubs():
    drone_map = make_map(
        [Connection(from_hub="start", to_hub="missing")]
    )

    with pytest.raises(ValueError, match="unknown hub"):
        GraphBuilder(drone_map).connectors_dic()
