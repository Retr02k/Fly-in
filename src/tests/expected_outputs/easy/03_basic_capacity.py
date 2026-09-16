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
        "bottleneck": {
            "name": "bottleneck",
            "x": 1,
            "y": 0,
            "zone_type": "normal",
            "color": "orange",
            "max_drones": 2,
        },
        "wide_area": {
            "name": "wide_area",
            "x": 2,
            "y": 0,
            "zone_type": "normal",
            "color": "blue",
            "max_drones": 3,
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
            "to_hub": "bottleneck",
            "max_link_capacity": 4,
         },
        {
            "from_hub": "bottleneck",
            "to_hub": "wide_area",
            "max_link_capacity": 4,
        },
        {
            "from_hub": "wide_area",
            "to_hub": "goal",
            "max_link_capacity": 4,
        },
    ],
}
