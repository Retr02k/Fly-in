from pathlib import Path
import sys
from typing import TextIO
from fly_in.model.drone import DroneStatus
from fly_in.parser import MapParser
from fly_in.simulation import Simulator
from fly_in.errors.custom_errors import MapParseError


_ANSI_COLORS = {
    "black": 30, "red": 31, "green": 32, "yellow": 33,
    "blue": 34, "purple": 35, "cyan": 36, "white": 37,
    "orange": 33, "brown": 33,
}


def _connection_label(origin: str, destination: str) -> str:
    return f"{origin}-{destination}"


def _render_map(simulator: Simulator, stream: TextIO, color: bool) -> None:
    parsed_map = simulator.parsed_map
    print(
        f"Turn {simulator.current_turn} | "
        f"{parsed_map.start_hub} -> {parsed_map.end_hub}",
        file=stream,
    )
    for hub_name, hub in sorted(
        parsed_map.hubs.items(),
        key=lambda item: (item[1].y, item[1].x, item[0]),
    ):
        drones = [
            str(drone.drone_id)
            for drone in simulator.drones
            if drone.status != DroneStatus.DELIVERED
            and drone.current_hub == hub_name
        ]
        marker = "*" if hub_name in (
            parsed_map.start_hub, parsed_map.end_hub,
        ) else " "
        label = f"{marker}{hub_name} [{hub.zone_type.value}]"
        ansi_color = _ANSI_COLORS.get(hub.color or "")
        if color and ansi_color is not None:
            label = f"\033[{ansi_color}m{label}\033[0m"
        print(f"  {label}: {', '.join(drones) or '-'}", file=stream)
    for drone in simulator.drones:
        if drone.status == DroneStatus.MOVING and drone.transit is not None:
            print(
                f"  D{drone.drone_id}-"
                f"{_connection_label(*drone.transit.connection)}",
                file=stream,
            )


def _turn_output(simulator: Simulator) -> str:
    lines = [f"\nTurn {simulator.current_turn} movement events:"]
    for drone_id, origin, destination in simulator.last_arrivals:
        lines.append(
            f"  D{drone_id} arrived at {destination} "
            f"(from {origin})."
        )
    for move in simulator.last_planned_moves:
        if move.duration > 1:
            lines.append(
                f"  D{move.drone.drone_id} departed {move.origin_hub} "
                f"towards {move.destination_hub}; "
                f"in transit on {_connection_label(*move.connection)} "
                f"({move.duration} turns)."
            )
        else:
            lines.append(
                f"  D{move.drone.drone_id} departed {move.origin_hub} "
                f"towards {move.destination_hub} "
                f"(arrival next turn)."
            )
    if len(lines) == 1:
        lines.append("  No drone movement.")
    return "\n".join(lines)


def _print_stats(simulator: Simulator, stream: TextIO) -> None:
    stats = simulator.stats
    print("\nSimulation statistics", file=stream)
    print(f"  Turns: {simulator.current_turn}", file=stream)
    print(f"  Total movement events: {stats.total_movements}", file=stream)
    print(
        f"  Average turns per drone: {stats.average_delivery_turns:.2f}",
        file=stream,
    )
    print(f"  Total path cost: {stats.total_path_cost}", file=stream)
    print(f"  Average path cost: {stats.average_path_cost:.2f}", file=stream)
    print(f"  Waiting turns: {sum(stats.waiting_turns.values())}", file=stream)
    print(f"  Restricted transits: {stats.restricted_transits}", file=stream)
    print(f"  Throughput: {stats.throughput:.2f} drones/turn", file=stream)
    print(
        f"  Route cache: {simulator.route_cache_hits} hits, "
        f"{simulator.route_cache_misses} misses",
        file=stream,
    )


def run_cli(
    map_path: str,
    *,
    step_mode: bool = False,
    color: bool = False,
    input_stream: TextIO = sys.stdin,
    output_stream: TextIO = sys.stdout,
    log_path: str | None = None,
) -> int:
    simulator = Simulator(MapParser(filepath=map_path).parse())
    log_stream: TextIO | None = None
    try:
        if log_path is not None:
            output_root = Path.cwd() / "output"
            output_root.mkdir(exist_ok=True)
            requested_path = Path(log_path)
            if requested_path.is_absolute():
                raise ValueError(
                    "Log path must be relative to the output directory."
                )
            resolved_path = (output_root / requested_path).resolve()
            if output_root.resolve() not in resolved_path.parents:
                raise ValueError(
                    "Log path must stay inside the output directory."
                )
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            log_stream = open(resolved_path, "w")
        try:
            while any(
                drone.status != DroneStatus.DELIVERED
                for drone in simulator.drones
            ):
                simulator.step()
                line = _turn_output(simulator)
                print(line, file=output_stream)
                if log_stream is not None:
                    print(line, file=log_stream)
                _render_map(simulator, output_stream, color)
                if step_mode and any(
                    drone.status != DroneStatus.DELIVERED
                    for drone in simulator.drones
                ):
                    print(
                        "Press Enter for the next turn...",
                        file=output_stream,
                    )
                    input_stream.readline()
            print(
                f"Delivered {len(simulator.drones)} drones in "
                f"{simulator.current_turn} turns.",
                file=output_stream,
            )
            _print_stats(simulator, output_stream)
            if log_stream is not None:
                print(
                    f"Delivered {len(simulator.drones)} drones in "
                    f"{simulator.current_turn} turns.",
                    file=log_stream,
                )
                _print_stats(simulator, log_stream)
        except KeyboardInterrupt:
            print(
                "\nSimulation interrupted by user.",
                file=output_stream,
            )
            if log_stream is not None:
                print("Simulation interrupted by user.", file=log_stream)
            return 130
    finally:
        if log_stream is not None:
            log_stream.close()
    return 0


def _choose_map(
    input_stream: TextIO,
    output_stream: TextIO,
) -> str | None:
    maps = sorted(Path("src/maps").glob("**/*.txt"))
    print("\nAvailable maps:", file=output_stream)
    for index, map_path in enumerate(maps, 1):
        print(f"  {index}. {map_path}", file=output_stream)
    print("  c. Custom map path", file=output_stream)
    choice = input_stream.readline().strip()
    if choice.lower() == "c":
        print("Enter the path to the map file:", file=output_stream)
        custom_path = input_stream.readline().strip()
        try:
            path = Path(custom_path)
            if not path.is_file():
                print(
                    "Map error: that file does not exist or is not a file.",
                    file=output_stream,
                )
                return None
            with path.open():
                pass
        except OSError as error:
            print(
                f"Map error: cannot read that file ({error}).",
                file=output_stream,
            )
            return None
        return custom_path
    if choice.isdigit() and 1 <= int(choice) <= len(maps):
        return str(maps[int(choice) - 1])
    return None


def main() -> None:
    input_stream, output_stream = sys.stdin, sys.stdout
    try:
        print("Fly-in simulation", file=output_stream)
        map_path = _choose_map(input_stream, output_stream)
        if map_path is None:
            raise SystemExit("Invalid map selection.")
        print("\n1. Complete run\n2. Step-by-step run", file=output_stream)
        mode = input_stream.readline().strip()
        if mode not in {"1", "2"}:
            raise SystemExit("Invalid run mode.")
        print("\nSave output log? [y/N]", file=output_stream)
        log_path: str | None = None
        if input_stream.readline().strip().lower() == "y":
            print(
                "Enter an output log filename inside the output/ directory:",
                file=output_stream,
            )
            log_path = input_stream.readline().strip()
        raise SystemExit(run_cli(
            map_path,
            step_mode=mode == "2",
            color=output_stream.isatty(),
            input_stream=input_stream,
            output_stream=output_stream,
            log_path=log_path,
        ))
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.", file=output_stream)
        raise SystemExit(130) from None
    except MapParseError as error:
        raise SystemExit(f"Map error: {error}") from error
    except (OSError, ValueError) as error:
        raise SystemExit(f"Unable to run simulation: {error}") from error
