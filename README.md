*This project has been created as part of the 42 curriculum by diosoare.*

# Fly-in

## Description

Fly-in is a drone fleet routing system. Given a network of interconnected hubs and a fleet of drones stationed at a starting hub, the goal is to move all drones to a designated end hub in the minimum number of simulation turns, while respecting capacity constraints on both hubs and connections.

The program reads a custom map file that defines the network topology, zone types, and capacity limits. It computes optimal routes using a max-flow algorithm, simulates the movement tick by tick, and renders the result in a fullscreen graphical interface.

## Algorithm and Implementation

**Pathfinding - Dinic's max-flow algorithm**

The routing problem is modeled as a flow network. Each hub is split into two nodes (in-node and out-node) connected by an internal edge whose capacity equals the hub's `max_drones` limit. This node-split technique enforces per-hub occupancy constraints within the standard max-flow framework.

Connections between hubs are added as bidirectional edges with their `max_link_capacity`. Priority zones are sorted to the front of the edge list so flow is directed through them first when capacity allows.

Dinic's algorithm is then run on this graph to determine the maximum number of drones that can be routed simultaneously from source to sink. The BFS phase builds a level graph; the DFS phase pushes blocking flow along shortest augmenting paths. This runs in O(V² · E) time, which is efficient for the map sizes used here.

**Tick simulation**

Once the level graph produces a set of valid paths, drones are assigned to routes and stepped forward one hub per turn. Each turn is a "tick". The simulation records which hub each drone occupies at every tick, producing a list of states used by the renderer.

**Zone types**

- `start` / `end`: source and sink of the flow network; capacity is treated as unlimited.
- `blocked`: excluded from the graph entirely; no flow passes through.
- `priority`: edges touching these hubs are evaluated first during flow routing.

## Instructions

**Requirements**

- Python 3.10 or later
- uv (Astral's Python package/project manager)

**Installation & Usage**

```bash
git clone https://github.com/Diogo-Serra/Fly-in
cd Fly-in
make start
```

This project uses uv for dependency management. The install target sets up uv and syncs dependencies from `pyproject.toml`.

The program presents an interactive menu:

```
1. Select Map        - choose a map file from src/maps/
2. See Map info      - display hub and drone details for the loaded map
3. Navigation System - run the pathfinder and open the visual renderer
0. Exit
```

**Solution output**

Each time the Navigation System runs, the computed drone routing is written to solution/<map_name>.txt at the project root. Each line represents one tick, listing drone moves (D<n>-<hub>) until all drones reach the goal.

**Map file format**

Map files are plain text and placed in `src/maps/`. Example:

```
# Easy: Simple linear path
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue max_drones=1]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1 [max_link_capacity=2]
connection: waypoint1-goal
```

Supported hub types: `start_hub`, `hub`, `end_hub`. Optional metadata keys: `color`, `max_drones`, `zone` (`blocked` or `priority`). Connection metadata key: `max_link_capacity`.

## Visual Representation

The renderer is built with pygame and runs fullscreen. It draws the hub network as a graph, with hubs as labeled circles and connections as lines between them.

During playback, each hub displays a badge showing how many drones currently occupy it. The drone count updates each tick so the flow of the fleet across the network is visible in real time.

**Controls**

| Key | Action |
|-----|--------|
| `P` | Play / pause |
| `→` | Step forward one turn (while paused) |
| `←` | Step back one turn (while paused) |
| `S` | Solution page in pygame |
| `R` | Reset to turn 1 |
| `L` | Toggle hub and edge labels |
| `ESC` | Quit |


The layout scales automatically to fill the screen regardless of map size.

## Resources

- Dinic's algorithm - [Baeldung](https://www.baeldung.com/cs/dinics)
- Dinic's algorithm - [Wikipedia](https://en.wikipedia.org/wiki/Dinic%27s_algorithm)
- Dinic's algorithm (video) - [YouTube](https://www.youtube.com/watch?v=FfWsCRIHnQ4)
- Dinic's algorithm (video 2) - [YouTube](https://www.youtube.com/watch?v=M6cm8UeeziI)
- pygame documentation - [https://www.pygame.org/docs/](https://www.pygame.org/docs/)
- pydantic documentation - [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
- uv documentation - [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

**AI usage**

AI (GitHub Copilot) was used during this project for the following tasks:
- Understanding and exploring Dinic's algorithm (BFS level graph, DFS blocking flow, node-split technique)
- Clarifying the correctness of the node-split construction for vertex-capacitated flow networks
- Reviewing edge case handling in the tick simulation (single-hub maps, blocked zones)
- Suggesting the priority-key sort to bias flow toward priority zones without modifying the algorithm itself
- Getting started with pygame (display setup, event loop, drawing primitives)
- Writing the documentation and organizing the README
