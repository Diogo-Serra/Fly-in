# Benchmark module for Fly-in

from .. import Map, Pathfinder
from . import ALL_MAPS, DEFAULT_MAP

BENCHMARKS = [
    ("Easy", "Linear path", "Simple Linear Path", 2, 6),
    ("Easy", "Simple fork", "Simple fork with two paths", 4, 8),
    ("Easy", "Basic capacity", "Basic capacity management", 4, 6),
    ("Medium", "Dead end trap",
     "Dead end trap - drones might get stuck", 5, 12),
    ("Medium", "Circular loop", "Circular loop with restricted zones", 6, 15),
    ("Medium", "Priority puzzle",
     "Priority zones create optimal path challenges", 5, 12),
    ("Hard", "Maze nightmare",
     "Complex maze with multiple dead ends and loops", 8, 30),
    ("Hard", "Capacity hell",
     "Extreme capacity constraints with timing challenges", 12, 35),
    ("Hard", "Ultimate challenge",
     "THE ULTIMATE CHALLENGE - All tricks combined", 15, 45),
    ("Challenger", "The Impossible Dream", "THE IMPOSSIBLE DREAM", 25, 45),
]

MAPS_BY_NAME = {**ALL_MAPS, "Simple Linear Path": DEFAULT_MAP}


def main() -> None:
    header = (f"{'Category':<10} {'Map':<22} {'Drones':>7} {'Target':>7} "
              f"{'Turns':>6} {'Flow':>5} {'Result':>7}")
    print(header)
    print("-" * len(header))
    for category, label, map_name, nb_drones, target in BENCHMARKS:
        map_data = dict(MAPS_BY_NAME[map_name])
        map_data["nb_drones"] = nb_drones
        nav_map = Map.model_validate(map_data)
        pf = Pathfinder(nav_map)
        turns = pf.total_ticks - 1
        status = "PASS" if turns <= target else "FAIL"
        print(f"{category:<10} {label:<22} {nb_drones:>7} {target:>7} "
              f"{turns:>6} {pf.flow_reached:>5} {status:>7}")


if __name__ == "__main__":
    main()
