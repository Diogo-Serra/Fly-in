from os import listdir
from pathlib import Path
from .maps import Hub, Map, Connection

try:
    from pydantic import BaseModel, Field, field_validator
except ImportError as error:
    print(error)


class FileHandler(BaseModel):
    filename: str
    name: str = ""
    nb_drones: int = 0
    difficulty: str = ""
    selected_map: Map | None = None
    hub_list: list[Hub] = Field(default_factory=lambda: list())
    connections: list[Connection] = Field(default_factory=lambda: list())

    @field_validator('filename', mode='after')
    def filename_validator(cls, filename: str) -> str:
        if filename not in listdir("src/maps/"):
            raise FileNotFoundError(
                f"Error: {filename} not found in src/maps/")
        return filename

    def read_map_file(self) -> Map:

        with open("src/maps/" + self.filename, 'r') as file:
            map_file: list[str] = file.read().split('\n')
        nb_drones_set = False

        for i, line in enumerate(map_file, start=1):
            if line.startswith('#'):
                if i == 1:
                    if ':' in line:
                        _difficulty, _name = tuple(line.split(':'))
                        self.difficulty = _difficulty.strip('# ')
                        self.name = _name.strip()
                continue

            if not line.strip():
                continue

            keyword = line.split(':', 1)[0].strip()
            if keyword not in {
                    'nb_drones', 'start_hub', 'hub', 'end_hub', 'connection'}:
                raise ValueError(
                    f"Line {i}: Invalid keyword '{keyword}'. "
                    f"Must be one of: "
                    f"nb_drones, start_hub, hub, end_hub, connection."
                )

            if line.startswith('nb_drones:'):
                self.nb_drones = int(line.split(':')[1].strip())
                nb_drones_set = True
                continue

            if not nb_drones_set:
                raise ValueError(
                    f"Line {i}: nb_drones must be defined before "
                    f"hubs/connections.")

            if line.startswith('start_hub:'):
                hub_data = line.split(':')[1].strip().split()
                meta = self.metadata_parser(
                    hub_data[3:], ignore_keys={'max_drones'}, line_num=i)
                meta['hub_type'] = 'start'
                self.hub_list.append(Hub.model_validate({
                    'name': hub_data[0],
                    'x': hub_data[1],
                    'y': hub_data[2],
                    'metadata': meta
                }))
                continue

            if line.startswith('end_hub:'):
                hub_data = line.split(':')[1].strip().split()
                meta = self.metadata_parser(
                    hub_data[3:], ignore_keys={'max_drones'}, line_num=i)
                meta['hub_type'] = 'end'
                self.hub_list.append(Hub.model_validate({
                    'name': hub_data[0],
                    'x': hub_data[1],
                    'y': hub_data[2],
                    'metadata': meta
                }))
                continue

            if line.startswith('hub:'):
                hub_data = line.split(':')[1].strip().split()
                self.hub_list.append(Hub.model_validate({
                    'name': hub_data[0],
                    'x': hub_data[1],
                    'y': hub_data[2],
                    'metadata': self.metadata_parser(
                        hub_data[3:], line_num=i)
                }))

            if line.startswith('connection:'):
                _connection = line.split(':')[1].strip().split()
                from_hub, to_hub = _connection[0].split('-', 1)
                self.connections.append(Connection(
                    from_hub=from_hub,
                    to_hub=to_hub,
                    metadata=self.metadata_parser(
                        _connection[1:], 'connection', line_num=i)
                ))

        hub_names = {hub.name for hub in self.hub_list}
        for conn in self.connections:
            if conn.from_hub not in hub_names:
                raise ValueError(
                    f"Invalid connection: "
                    f"hub '{conn.from_hub}' does not exist."
                )
            if conn.to_hub not in hub_names:
                raise ValueError(
                    f"Invalid connection: hub '{conn.to_hub}' does not exist."
                )

        if self.nb_drones <= 0:
            raise ValueError("nb_drones must be a positive integer.")

        names = [h.name for h in self.hub_list]
        if len(names) != len(set(names)):
            dupes = sorted({n for n in names if names.count(n) > 1})
            raise ValueError(f"Duplicate hub name(s): {', '.join(dupes)}.")

        start_count = sum(
            h.metadata.get('hub_type') == 'start' for h in self.hub_list)
        end_count = sum(
            h.metadata.get('hub_type') == 'end' for h in self.hub_list)
        if start_count != 1:
            raise ValueError(
                f"Map must have exactly one start_hub, found {start_count}.")
        if end_count != 1:
            raise ValueError(
                f"Map must have exactly one end_hub, found {end_count}.")

        self.selected_map = Map(
            name=self.name,
            hub_list=self.hub_list,
            difficulty=self.difficulty,
            nb_drones=self.nb_drones,
            connections=self.connections)
        return self.selected_map

    @staticmethod
    def metadata_parser(
        metadata: list[str],
        context: str = 'hub',
        ignore_keys: set[str] | None = None,
        line_num: int = 0
    ) -> dict[str, str]:
        valid_zone_types = {'normal', 'blocked', 'restricted', 'priority'}
        capacity_keys = {'max_drones', 'max_link_capacity'}
        valid_keys: dict[str, set[str]] = {
            'hub': {'zone', 'color', 'max_drones'},
            'connection': {'max_link_capacity'},
        }
        allowed_keys = valid_keys.get(context, set())
        _ignore = ignore_keys or set()
        prefix = f"Line {line_num}: " if line_num else ""
        metadata_dict: dict[str, str] = {}
        for pair in metadata:
            key, value = pair.strip('[]').split('=')
            key, value = key.strip(), value.strip()
            if key in _ignore:
                continue
            if key not in allowed_keys:
                raise ValueError(
                    f"{prefix}Invalid metadata key '{key}' "
                    f"for {context}. Must be one of: "
                    f"{', '.join(sorted(allowed_keys - _ignore))}."
                )
            if key in capacity_keys:
                if not value.isdigit() or int(value) < 1:
                    raise ValueError(
                        f"{prefix}'{key}' must be a positive integer, "
                        f"got '{value}'."
                    )
            metadata_dict[key] = value
        zone = metadata_dict.get('zone')
        if zone is not None and zone not in valid_zone_types:
            raise ValueError(
                f"{prefix}Invalid zone type '{zone}'. "
                f"Must be one of: {', '.join(sorted(valid_zone_types))}."
            )
        return metadata_dict

    def write_solution(self, ticks: list[list[str]], end_name: str) -> None:
        nav_map = self.selected_map
        if nav_map is None:
            return
        num_drones = nav_map.nb_drones
        zone_of = {
            h.name: h.metadata.get('zone', '')
            for h in nav_map.hub_list
        }
        conn_id: dict[tuple[str, str], str] = {}
        for conn in nav_map.connections:
            conn_id[(conn.from_hub, conn.to_hub)] = (
                f"{conn.from_hub}-{conn.to_hub}")
            conn_id[(conn.to_hub, conn.from_hub)] = (
                f"{conn.to_hub}-{conn.from_hub}")

        delivered: set[int] = set()
        lines: list[str] = []

        for tick in range(1, len(ticks)):
            prev_tick, curr_tick = ticks[tick - 1], ticks[tick]
            moves: list[str] = []
            for drone_idx in range(num_drones):
                if drone_idx in delivered:
                    continue
                prev_hub, curr_hub = prev_tick[drone_idx], curr_tick[drone_idx]
                if curr_hub == end_name:
                    delivered.add(drone_idx)
                    moves.append(f"D{drone_idx + 1}-{end_name}")
                elif prev_hub != curr_hub:
                    if zone_of.get(curr_hub) == 'restricted':
                        label = conn_id.get((prev_hub, curr_hub), curr_hub)
                    else:
                        label = curr_hub
                    moves.append(f"D{drone_idx + 1}-{label}")
            if moves:
                lines.append(" ".join(moves))

        root = Path(__file__).parent.parent.parent
        name = nav_map.name.replace(' ', '_').lower()
        out = root / "solution" / f"{name}.txt"
        out.parent.mkdir(exist_ok=True)
        out.write_text("\n".join(lines) + ("\n" if lines else ""))
