# Bootstrap module

from .app import run
from pathlib import Path
from .classes import DEFAULT_MAP
from .classes import FileHandler, Map

try:
    from pydantic import ValidationError
except ImportError as error:
    print(error)
    exit(1)


def ensure_default_map() -> None:
    maps_dir = Path(__file__).parent.parent / "maps"
    has_map_files = maps_dir.is_dir() and any(maps_dir.glob("*.txt"))
    if not has_map_files:
        FileHandler.write_map_file(Map.model_validate(DEFAULT_MAP))


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
