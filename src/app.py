# Application controller

from .classes import FileHandler, Map, Renderer, Pathfinder
from os import listdir, system


def run(script: str | None = None) -> int:

    path_maps: str = "./maps/"
    _map: Map | None = None
    handler: FileHandler | None = None

    MENU: str = """
            === Fly-in - Drone System ===

            1. Select Map
            2. See Map info
            3. Navigation System
            0. Exit

    """

    system("clear")
    while True:
        choice: str = input(MENU + "Select option: ").strip()

        system("clear")
        match choice:

            case "1":
                map_file: str | None = map_menu(path_maps)
                if map_file is None:
                    print("Select a map first (option 1).")
                    continue
                handler = FileHandler(filename=map_file)
                _map = handler.read_map_file()
                print(f"Map Selected: {_map.name}")
            case "2":
                if not _map:
                    print("Select a map first (option 1).")
                else:
                    _map.map_info()
            case "3":
                if not _map or not handler:
                    print("Select a map first (option 1).")
                    continue
                pf = Pathfinder(_map)
                if pf.flow_reached == 0:
                    print("No solution possible on this map. Try another one.")
                    input("Press Enter to continue...")
                    continue
                handler.write_solution(pf.ticks, pf.end_name)
                Renderer(_map, pf).run()
            case "0":
                break
            case _:
                print("Invalid option")
    return 0


def map_menu(path_maps: str) -> str | None:

    maps_list: list[tuple[int, str]] = []

    sorted_maps = sorted(listdir(path_maps), key=lambda name: name[:2])
    for i, _map in enumerate(sorted_maps, start=1):
        maps_list.append((i, _map))

    while True:

        system("clear")
        print("=== Select Map ===\n")
        for index, map_name in maps_list:
            print(f"{index}. {map_name}")
        print("0. Back")

        user_input = input("\nSelect Map: ").strip()

        if user_input == "0":
            system("clear")
            break

        for index, map_name in maps_list:
            if str(index) == user_input:
                system("clear")
                return map_name

        system("clear")
        print("\nInvalid selection.")
        input("Press Enter to continue...")
    return None
