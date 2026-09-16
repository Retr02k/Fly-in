EXPECTED_MAP = {
    "nb_drones": 4,
    "start_hub": "start",
    "end_hub": "goal",
    "hubs": {
        "start": {
            "name": "start",
            "x": 0,
            "y": 0,
            "zone_type": "normal",
            "color": "green",
            "max_drones": 1,
        },
        "junction" : {
            "name": "junction",
            "x": 1,
            "y": 0,
            "zone_type": "normal",
            "color": "yellow",
            "max_drones": 2,
        },
        "path_a": {
            "name": "path_a",
            "x": 2,
            "y": 1,
            "zone_type": "normal",
            "color": "blue",
            "max_drones": 1,
        },
        "path_b": {
            "name": "path_b",
            "x": 2,
            "y": -1,
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
            "to_hub": "junction",
            "max_link_capacity": 2,
        },
        {
            "from_hub": "junction",
            "to_hub": "path_a",
            "max_link_capacity": 1,
        },
        {
            "from_hub": "junction",
            "to_hub": "path_b",
            "max_link_capacity": 1,
        },
        {
            "from_hub": "path_a",
            "to_hub": "goal",
            "max_link_capacity": 1,
        },
        {
            "from_hub": "path_b",
            "to_hub": "goal",
            "max_link_capacity": 1,
        },
    ],
}
