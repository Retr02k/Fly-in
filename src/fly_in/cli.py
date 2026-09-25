import argparse
import sys
from typing import TextIO

from fly_in.model.drone import DroneStatus
from fly_in.parser import MapParser
from fly_in.simulation import Simulator


_ANSI_COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "purple": 35,
    "cyan": 36,
    "white": 37,
    "orange": 33,
    "brown": 33,
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
            parsed_map.start_hub,
            parsed_map.end_hub,
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


def run_cli(
    map_path: str,
    *,
    step_mode: bool = False,
    color: bool = False,
    input_stream: TextIO = sys.stdin,
    output_stream: TextIO = sys.stdout,
) -> int:
    simulator = Simulator(MapParser(filepath=map_path).parse())
    while any(
        drone.status != DroneStatus.DELIVERED
        for drone in simulator.drones
    ):
        arrivals = simulator.step()
        movements = [
            f"D{drone.drone_id}-{destination}"
            for drone_id, _, destination in arrivals
            for drone in simulator.drones
            if drone.drone_id == drone_id
        ]
        movements.extend(
            f"D{drone.drone_id}-"
            f"{_connection_label(*drone.transit.connection)}"
            if drone.transit is not None
            else f"D{drone.drone_id}-{drone.current_hub}"
            for drone in simulator.drones
            if drone.status == DroneStatus.MOVING
        )
        print(
            f"Turn {simulator.current_turn}: "
            f"{' '.join(sorted(set(movements))) or '-'}",
            file=output_stream,
        )
        _render_map(simulator, output_stream, color)
        if step_mode and any(
            drone.status != DroneStatus.DELIVERED
            for drone in simulator.drones
        ):
            input_stream.readline()
    print(
        f"Delivered {len(simulator.drones)} drones in "
        f"{simulator.current_turn} turns.",
        file=output_stream,
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Fly-in simulation.")
    parser.add_argument("map_path", help="Path to a Fly-in map file.")
    parser.add_argument(
        "--step",
        action="store_true",
        help="Wait for Enter between simulation turns.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors in the map view.",
    )
    args = parser.parse_args()
    raise SystemExit(
        run_cli(
            args.map_path,
            step_mode=args.step,
            color=not args.no_color and sys.stdout.isatty(),
        )
    )
