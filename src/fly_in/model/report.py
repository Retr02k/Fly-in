from dataclasses import dataclass, field


@dataclass
class SimulationStats:
    movement_counts: list[int] = field(default_factory=list)
    delivery_turns: dict[int, int] = field(default_factory=dict)
    waiting_turns: dict[int, int] = field(default_factory=dict)
    path_costs: dict[int, int] = field(default_factory=dict)
    restricted_transits: int = 0

    @property
    def total_movements(self) -> int:
        return sum(self.movement_counts)

    @property
    def average_delivery_turns(self) -> float:
        return (
            sum(self.delivery_turns.values()) / len(self.delivery_turns)
            if self.delivery_turns else 0.0
        )

    @property
    def total_path_cost(self) -> int:
        return sum(self.path_costs.values())

    @property
    def average_path_cost(self) -> float:
        return (
            self.total_path_cost / len(self.path_costs)
            if self.path_costs else 0.0
        )

    @property
    def throughput(self) -> float:
        return (
            len(self.delivery_turns) / len(self.movement_counts)
            if self.movement_counts else 0.0
        )
