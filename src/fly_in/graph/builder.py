from fly_in.model.map import Map


class GraphBuilder:
    def __init__(self, drone_map: Map) -> None:
        self.drone_map = drone_map

    def _validate_connections(self) -> None:
        hub_names = set(self.drone_map.hubs)
        for connection in self.drone_map.connections:
            missing_hubs = {
                connection.from_hub,
                connection.to_hub,
            } - hub_names
            if missing_hubs:
                missing = ", ".join(sorted(missing_hubs))
                raise ValueError(
                    f"Connection references unknown hub(s): {missing}"
                )

    def hub_matrix(self):
        nb_vertices = len(self.drone_map.hubs)
        matrix = [[0] * nb_vertices for _ in range(nb_vertices)]
        min_x, max_x = min(self.drone_map.hubs[hub_name].x for hub_name in self.drone_map.hubs.keys()), max(self.drone_map.hubs[hub_name].x for hub_name in self.drone_map.hubs.keys())
        min_y, max_y = min(self.drone_map.hubs[hub_name].y for hub_name in self.drone_map.hubs.keys()), max(self.drone_map.hubs[hub_name].y for hub_name in self.drone_map.hubs.keys())

        for hub_name in self.drone_map.hubs.keys():
            hub_x, hub_y = self.drone_map.hubs[hub_name].x, self.drone_map.hubs[hub_name].y
            normalized_hub_x, normalized_hub_y = hub_x - min_x, hub_y - min_y
            matrix[normalized_hub_x][normalized_hub_y] = 1
        return matrix

    def connectors_dic(self) -> dict[str, dict[str, int]]:
        self._validate_connections()
        connec_dict: dict[str, dict[str, int]] = {
            hub_name: {} for hub_name in self.drone_map.hubs
        }

        for connection in self.drone_map.connections:
            connec_dict[connection.from_hub][connection.to_hub] = (
                connection.max_link_capacity
            )
            connec_dict[connection.to_hub][connection.from_hub] = (
                connection.max_link_capacity
            )

        return connec_dict
