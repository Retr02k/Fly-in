from io import StringIO

from fly_in.cli import run_cli


def test_cli_runs_map_and_reports_delivery() -> None:
    output = StringIO()

    result = run_cli(
        "src/maps/easy/01_linear_path.txt",
        output_stream=output,
    )

    rendered = output.getvalue()
    assert result == 0
    assert "Turn 1:" in rendered
    assert "D1-start-waypoint1" in rendered
    assert "Delivered 2 drones" in rendered
