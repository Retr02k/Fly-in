from enum import Enum


class ZoneType(str, Enum):
    """Classify the movement behavior of a map hub."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
