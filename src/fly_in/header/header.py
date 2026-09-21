from enum import Enum


class ZoneType(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class DroneStatus(int, Enum):
    WAITING = 0
    MOVING = 1
    DELIVERED = 2

