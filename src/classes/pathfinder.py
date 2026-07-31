# Pathfinder - Dinic max-flow + tick-by-tick drone simulation

from .map import Connection, Map
from collections import defaultdict, deque


class Pathfinder:
    INF = 10 ** 9

    def __init__(self, nav_map: Map) -> None:
        self.nav_map = nav_map
        self.ticks: list[list[str]] = []
        self.total_ticks: int = 0
        self.flow_reached: int = 0
        self.end_name: str = ""
        self._solve()

    # Dinic's helpers

    def _add_edge(self, from_node: int, to_node: int, capacity: int) -> None:
        self._graph[from_node].append(
            [to_node, capacity, len(self._graph[to_node])]
        )
        self._graph[to_node].append(
            [from_node, 0, len(self._graph[from_node]) - 1]
        )

    def _bfs(self, source: int, sink: int) -> bool:
        self._level = [-1] * len(self._graph)
        self._level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for neighbor, capacity, _ in self._graph[node]:
                if capacity > 0 and self._level[neighbor] < 0:
                    self._level[neighbor] = self._level[node] + 1
                    queue.append(neighbor)
        return self._level[sink] >= 0

    def _dfs(self, source: int, sink: int, flow_limit: int) -> int:
        node_path = [source]
        edge_path: list[list[int]] = []

        while node_path:
            node = node_path[-1]
            if node == sink:
                flow_sent = min([flow_limit] + [e[1] for e in edge_path])
                for edge in edge_path:
                    edge[1] -= flow_sent
                    self._graph[edge[0]][edge[2]][1] += flow_sent
                self._record_path(node_path, flow_sent)
                return flow_sent

            while self._next_edge[node] < len(self._graph[node]):
                edge = self._graph[node][self._next_edge[node]]
                neighbor, capacity, _ = edge
                if (capacity > 0
                        and self._level[neighbor] == self._level[node] + 1):
                    node_path.append(neighbor)
                    edge_path.append(edge)
                    break
                self._next_edge[node] += 1
            else:
                node_path.pop()
                if edge_path:
                    edge_path.pop()
                    self._next_edge[node_path[-1]] += 1
        return 0

    # Dinic and path recorder

    def _dinic(self, source: int, sink: int, limit: int) -> int:
        total_flow = 0
        while total_flow < limit and self._bfs(source, sink):
            self._next_edge = [0] * len(self._graph)
            while flow_sent := self._dfs(source, sink, limit - total_flow):
                total_flow += flow_sent
        return total_flow

    def _record_path(self, node_path: list[int], flow_sent: int) -> None:
        hub_seq = [self._hub_names[node % self._num_hubs]
                   for node in node_path]
        path = [hub_seq[0]]
        for name in hub_seq[1:]:
            if name != path[-1]:
                path.append(name)
        self._paths.extend([path] * flow_sent)

    # Build graph and route flow

    def _solve(self) -> None:
        hubs = self.nav_map.hub_list
        num_hubs = len(hubs)
        hub_index = {h.name: i for i, h in enumerate(hubs)}
        hub_names = [h.name for h in hubs]

        start = next((h for h in hubs if h.hub_type == 'start'), None)
        end = next((h for h in hubs if h.hub_type == 'end'), None)

        if not start or not end:
            num_drones = self.nav_map.nb_drones
            self.ticks = [[hub_names[0]] * num_drones]
            self.total_ticks = 1
            return

        source_idx, sink_idx = hub_index[start.name], hub_index[end.name]

        zones = [h.zone for h in hubs]
        blocked_hubs = {i for i, z in enumerate(zones) if z == 'blocked'}
        priority_names = {
            hubs[i].name for i, z in enumerate(zones) if z == 'priority'
        }

        choke_names = {
            h.name for h in hubs
            if h.zone == 'restricted' or h.capacity == 1
        }

        # Node-split graph: each hub i becomes i (in) and num_hubs+i (out)

        self._graph: list[list[list[int]]] = [[] for _ in range(2 * num_hubs)]
        for i, hub in enumerate(hubs):
            if i in blocked_hubs:
                continue
            capacity = (self.INF if i in (source_idx, sink_idx)
                        else hub.capacity or self.INF)
            self._add_edge(i, num_hubs + i, capacity)

        def _priority_key(conn: Connection) -> int:
            if conn.touches(priority_names):
                return 0
            return 2 if conn.touches(choke_names) else 1

        for conn in sorted(self.nav_map.connections, key=_priority_key):
            hub_a, hub_b = hub_index[conn.from_hub], hub_index[conn.to_hub]
            if hub_a in blocked_hubs or hub_b in blocked_hubs:
                continue
            capacity = conn.capacity or self.INF
            self._add_edge(num_hubs + hub_a, hub_b, capacity)
            self._add_edge(num_hubs + hub_b, hub_a, capacity)

        # Run Dinic max-flow capped at nb_drones

        self._num_hubs = num_hubs
        self._hub_names = hub_names
        self._paths: list[list[str]] = []
        self.flow_reached = self._dinic(
            num_hubs + source_idx, sink_idx, self.nav_map.nb_drones
        )

        self._simulate(
            self._paths, hub_names[source_idx], hub_names[sink_idx])

    # Tick-by-tick simulation

    def _simulate(
        self,
        paths: list[list[str]],
        start_name: str,
        end_name: str,
    ) -> None:
        self.end_name = end_name
        num_drones = self.nav_map.nb_drones

        if not paths:
            self.ticks = [[start_name] * num_drones]
            self.total_ticks = 1
            return

        drone_paths = [paths[i % len(paths)] for i in range(num_drones)]
        final_step = [len(path) - 1 for path in drone_paths]

        zone_of = {h.name: h.zone for h in self.nav_map.hub_list}
        hub_cap: dict[str, int] = {
            h.name: h.capacity or self.INF
            for h in self.nav_map.hub_list
        }
        hub_cap[start_name] = hub_cap[end_name] = self.INF
        link_cap: dict[tuple[str, str], int] = {}
        for conn in self.nav_map.connections:
            cap = conn.capacity or self.INF
            link_cap[(conn.from_hub, conn.to_hub)] = cap
            link_cap[(conn.to_hub, conn.from_hub)] = cap

        drone_pos = [0] * num_drones
        in_transit = [False] * num_drones
        ticks = [[drone_paths[i][0] for i in range(num_drones)]]
        MAX_TICKS = (
            (max(len(p) for p in drone_paths) + num_drones) * (num_drones + 4)
        )

        for _ in range(MAX_TICKS):
            if all(
                drone_pos[i] == final_step[i] and not in_transit[i]
                for i in range(num_drones)
            ):
                break

            just_arrived: set[int] = set()
            for i in range(num_drones):
                if in_transit[i]:
                    drone_pos[i] += 1
                    in_transit[i] = False
                    just_arrived.add(i)

            hub_occ: defaultdict[str, int] = defaultdict(int)
            for i in range(num_drones):
                hub_occ[drone_paths[i][drone_pos[i]]] += 1

            link_occ: defaultdict[tuple[str, str], int] = defaultdict(int)
            reserved: defaultdict[str, int] = defaultdict(int)

            for i in sorted(
                range(num_drones),
                key=lambda i: final_step[i] - drone_pos[i]
            ):
                if drone_pos[i] == final_step[i] or i in just_arrived:
                    continue
                cur = drone_paths[i][drone_pos[i]]
                nxt = drone_paths[i][drone_pos[i] + 1]
                link_key = (cur, nxt)
                hub_ok = (
                    hub_occ[nxt] + reserved[nxt]
                    < hub_cap.get(nxt, self.INF)
                )
                link_ok = link_occ[link_key] < link_cap.get(link_key, self.INF)
                if hub_ok and link_ok:
                    hub_occ[cur] -= 1
                    link_occ[link_key] += 1
                    if zone_of.get(nxt) == 'restricted':
                        reserved[nxt] += 1
                        in_transit[i] = True
                    else:
                        hub_occ[nxt] += 1
                        drone_pos[i] += 1

            ticks.append(
                [drone_paths[i][drone_pos[i]] for i in range(num_drones)]
            )

        self.ticks = ticks
        self.total_ticks = len(ticks)
