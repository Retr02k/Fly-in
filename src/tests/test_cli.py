from io import StringIO
from pathlib import Path
from types import SimpleNamespace

import pytest

import fly_in.cli as cli
from fly_in.cli import _choose_map, run_cli
from fly_in.model.drone import DroneStatus


def test_cli_runs_map_and_reports_delivery() -> None:
    output = StringIO()

    result = run_cli(
        "src/maps/easy/01_linear_path.txt",
        output_stream=output,
    )

    rendered = output.getvalue()
    assert result == 0
    assert "Turn 1 movement events:" in rendered
    assert "D1 departed start towards waypoint1" in rendered
    assert "D1 arrived at goal" in rendered
    assert "Delivered 2 drones" in rendered
    assert "Simulation statistics" in rendered


def test_cli_overwrites_requested_log(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    log_path = Path("simulation.log")
    log_path.write_text("old content")
    map_path = (
        Path(__file__).resolve().parents[2]
        / "src/maps/easy/01_linear_path.txt"
    )

    run_cli(
        str(map_path),
        output_stream=StringIO(),
        log_path=str(log_path),
    )

    content = (tmp_path / "output" / "simulation.log").read_text()
    assert "old content" not in content
    assert "Delivered 2 drones in 5 turns." in content


def test_custom_map_selection_prompts_for_path() -> None:
    output = StringIO()
    selected = _choose_map(
        StringIO("c\nsrc/maps/easy/01_linear_path.txt\n"),
        output,
    )

    assert selected == "src/maps/easy/01_linear_path.txt"
    assert "Enter the path to the map file:" in output.getvalue()


def test_log_path_cannot_escape_output_directory(tmp_path: Path) -> None:
    output = StringIO()

    try:
        run_cli(
            "src/maps/easy/01_linear_path.txt",
            output_stream=output,
            log_path="../unsafe.log",
        )
    except ValueError as error:
        assert "inside the output directory" in str(error)
    else:
        raise AssertionError("Unsafe log path was accepted")


def test_cli_handles_keyboard_interrupt_and_closes_log(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class InterruptingSimulator:
        def __init__(self, parsed_map: object) -> None:
            self.drones = [
                SimpleNamespace(status=DroneStatus.WAITING),
            ]

        def step(self) -> None:
            raise KeyboardInterrupt

    monkeypatch.setattr(cli, "Simulator", InterruptingSimulator)
    monkeypatch.chdir(tmp_path)
    output = StringIO()
    result = run_cli(
        str(
            Path(__file__).resolve().parents[2]
            / "src/maps/easy/01_linear_path.txt"
        ),
        output_stream=output,
        log_path="interrupted.log",
    )

    assert result == 130
    assert "Simulation interrupted by user." in output.getvalue()
    log = tmp_path / "output" / "interrupted.log"
    assert log.read_text() == "Simulation interrupted by user.\n"
