# Bootstrap module

from .app import run
from pathlib import Path
from .classes import FileHandler, Map
from .classes import DEFAULT_MAP, ALL_MAPS, MAP_NAMES

try:
    from pydantic import ValidationError
except ImportError as error:
    print(error)
    exit(1)


def ensure_default_map() -> None:
    maps_dir = Path(__file__).parent.parent / "maps"
    has_map_files = maps_dir.is_dir() and any(maps_dir.glob("*.txt"))
    if not has_map_files:
        for map_data in ALL_MAPS.values():
            nav_map = Map.model_validate(map_data)
            _name = MAP_NAMES.get(nav_map.name)
            FileHandler.write_map_file(
                nav_map, filename=f"{_name}.txt" if _name else None)
        default_map = Map.model_validate(DEFAULT_MAP)
        _name = MAP_NAMES.get(default_map.name)
        FileHandler.write_map_file(
            default_map, filename=f"{_name}.txt" if _name else None)


def initialize(argv: list[str]) -> None:
    try:
        argv = [arg.strip() for arg in argv]
        script = argv[0]
        if script == "fly-in.py":
            ensure_default_map()
            run(script)
        else:
            print("Incorrect script name\nUsage:make start")
    except ValidationError as error:
        for _error in error.errors():
            if _error['loc']:
                print(f"Validation error at: {_error['loc'][0]}")
            print(f"Message: {_error['msg']}")
        print("Check your map file format.")
    except (FileNotFoundError, PermissionError) as error:
        print(f"File error: {error}")
    except ValueError as error:
        print(f"Value error: {error}")
    except (Exception, BaseException) as error:
        print(f"Unexpected error: {error}")
