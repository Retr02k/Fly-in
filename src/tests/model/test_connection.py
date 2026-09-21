from fly_in.model.connection import Connection


def test_connection_creates_with_from_and_to() -> None:
    conn = Connection(from_hub="start", to_hub="waypoint1")
    assert conn.from_hub == "start"
    assert conn.to_hub == "waypoint1"
