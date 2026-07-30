# Classes for Fly-in
from re import fullmatch

try:
    from pydantic import BaseModel, Field, field_validator
except ImportError as error:
    print(error)
    exit(1)


class Hub(BaseModel):
    name: str = Field(min_length=1)
    x: int = Field(default=0)
    y: int = Field(default=0)
    metadata: dict[str, str]

    @field_validator('name', mode='after')
    def validate_name(cls, name: str) -> str:
        if not fullmatch(r'[^\s-]+', name):
            raise ValueError(
                f"Invalid hub name '{name}': "
                "cannot contain spaces or dashes."
            )
        return name

    @property
    def capacity(self) -> int | None:
        cap = self.metadata.get('max_drones')
        return int(cap) if cap else None

    @property
    def zone(self) -> str:
        return self.metadata.get('zone', '')

    @property
    def hub_type(self) -> str:
        return self.metadata.get('hub_type', '')


class Connection(BaseModel):
    from_hub: str
    to_hub: str
    metadata: dict[str, str]

    @property
    def capacity(self) -> int | None:
        cap = self.metadata.get('max_link_capacity')
        return int(cap) if cap else None

    def touches(self, names: set[str]) -> bool:
        return self.from_hub in names or self.to_hub in names


class Map(BaseModel):
    hub_list: list[Hub]
    nb_drones: int
    name: str = Field(default='Mistery Map')
    difficulty: str = Field(default='Secret difficulty')
    connections: list[Connection] = Field(default_factory=list)

    def map_info(self) -> None:
        print("\n=== Map Info ===  ")
        print(f"{self.name} - {self.difficulty} : {self.nb_drones} Drones")
        for hub in self.hub_list:
            print()
            print(hub)
