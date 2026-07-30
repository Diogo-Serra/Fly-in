# Bootstrap module
from .app import run

try:
    from pydantic import ValidationError
except ImportError as error:
    print(error)
    exit(1)


def initialize(argv: list[str]) -> None:
    try:
        argv = [arg.strip() for arg in argv]
        script = argv[0]
        if script == "fly-in.py":
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
