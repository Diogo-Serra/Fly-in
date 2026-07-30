# Fly-in entry point
from sys import argv
from src import initialize


def main() -> None:
    if len(argv) == 1:
        initialize(argv)
    else:
        print("\nIncorrect start of Fly-in\n"
              "Usage:make start\n")


if __name__ == "__main__":
    main()
