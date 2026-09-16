EXPECTED_MAP = {
    "nb_drones": 2,
    "start_hub": "start",
    "end_hub": "goal",
    "hubs": {
        "start": {
            "name": "start",
            "x": 0,
            "y": 0,
            "zone_type": "normal",
            "color": "green",
            "max_drones": 5,
        },
        "waypoint1": {
            "name": "waypoint1",
            "x": 1,
            "y": 0,
            "zone_type": "normal",
            "color": "blue",
            "max_drones": 1,
        },
        "waypoint2": {
            "name": "waypoint2",
            "x": 2,
            "y": 0,
            "zone_type": "normal",
            "color": "blue",
            "max_drones": 1,
        },
        "goal": {
            "name": "goal",
            "x": 3,
            "y": 0,
            "zone_type": "normal",
            "color": "red",
            "max_drones": 1,
        },
    },
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "waypoint1",
            "max_link_capacity": 1,
        },
        {
            "from_hub": "waypoint1",
            "to_hub": "waypoint2",
            "max_link_capacity": 1,
        },
        {
            "from_hub": "waypoint2",
            "to_hub": "goal",
            "max_link_capacity": 1,
        },
    ],
}