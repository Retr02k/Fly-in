from dataclasses import dataclass, field


@dataclass
class SimulationStats:
    """Accumulate metrics produced during a simulation run.

    Attributes:
        movement_counts: Movement-event count for each turn.
        delivery_turns: Delivery turn indexed by drone ID.
        waiting_turns: Number of turns spent waiting by drone ID.
        path_costs: Weighted travelled cost indexed by drone ID.
        restricted_transits: Number of restricted departures.
    """
    movement_counts: list[int] = field(default_factory=list)
    delivery_turns: dict[int, int] = field(default_factory=dict)
    waiting_turns: dict[int, int] = field(default_factory=dict)
    path_costs: dict[int, int] = field(default_factory=dict)
    restricted_transits: int = 0

    @property
    def total_movements(self) -> int:
        """Return the total number of movement events."""
        return sum(self.movement_counts)

    @property
    def average_delivery_turns(self) -> float:
        """Return the average turn on which drones were delivered."""
        return (
            sum(self.delivery_turns.values()) / len(self.delivery_turns)
            if self.delivery_turns else 0.0
        )

    @property
    def total_path_cost(self) -> int:
        """Return the sum of weighted costs for all drone routes."""
        return sum(self.path_costs.values())

    @property
    def average_path_cost(self) -> float:
        """Return the average weighted route cost per drone."""
        return (
            self.total_path_cost / len(self.path_costs)
            if self.path_costs else 0.0
        )

    @property
    def throughput(self) -> float:
        """Return the average number of deliveries per simulation turn."""
        return (
            len(self.delivery_turns) / len(self.movement_counts)
            if self.movement_counts else 0.0
        )
