# Maps to use on Fly-in

from typing import Any

# Default Map

DEFAULT_MAP: dict[str, Any] = {
    "name": "Simple Linear Path",
    "difficulty": "Easy",
    "nb_drones": 2,
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {"hub_type": "start", "color": "green"},
        },
        {
            "name": "waypoint1",
            "x": 1,
            "y": 0,
            "metadata": {"color": "blue"},
        },
        {
            "name": "waypoint2",
            "x": 2,
            "y": 0,
            "metadata": {"color": "blue"},
        },
        {
            "name": "goal",
            "x": 3,
            "y": 0,
            "metadata": {"hub_type": "end", "color": "red"},
        },
    ],
    "connections": [
        {"from_hub": "start", "to_hub": "waypoint1", "metadata": {}},
        {"from_hub": "waypoint1", "to_hub": "waypoint2", "metadata": {}},
        {"from_hub": "waypoint2", "to_hub": "goal", "metadata": {}},
    ],
}
# Example maps

MAP_01_DEAD_END_TRAP: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "junction",
            "x": 1,
            "y": 0,
            "metadata": {
                "color": "yellow",
                "max_drones": "2",
            },
        },
        {
            "name": "dead_end",
            "x": 1,
            "y": 1,
            "metadata": {
                "color": "red",
            },
        },
        {
            "name": "correct_path",
            "x": 2,
            "y": 0,
            "metadata": {
                "color": "blue",
            },
        },
        {
            "name": "intermediate",
            "x": 3,
            "y": 0,
            "metadata": {
                "color": "blue",
            },
        },
        {
            "name": "goal",
            "x": 4,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 5,
    "name": "Dead end trap - drones might get stuck",
    "difficulty": "Medium Level 1",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "junction",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "junction",
            "to_hub": "dead_end",
            "metadata": {
            },
        },
        {
            "from_hub": "junction",
            "to_hub": "correct_path",
            "metadata": {
            },
        },
        {
            "from_hub": "correct_path",
            "to_hub": "intermediate",
            "metadata": {
            },
        },
        {
            "from_hub": "intermediate",
            "to_hub": "goal",
            "metadata": {
            },
        },
    ],
}

MAP_01_MAZE_NIGHTMARE: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "maze_a1",
            "x": 1,
            "y": 0,
            "metadata": {
                "color": "blue",
                "max_drones": "2",
            },
        },
        {
            "name": "maze_a2",
            "x": 2,
            "y": 0,
            "metadata": {
                "color": "blue",
            },
        },
        {
            "name": "maze_b1",
            "x": 1,
            "y": 1,
            "metadata": {
                "color": "blue",
            },
        },
        {
            "name": "maze_b2",
            "x": 2,
            "y": 1,
            "metadata": {
                "color": "blue",
                "max_drones": "2",
            },
        },
        {
            "name": "maze_c1",
            "x": 1,
            "y": 2,
            "metadata": {
                "color": "blue",
            },
        },
        {
            "name": "maze_c2",
            "x": 3,
            "y": 1,
            "metadata": {
                "color": "blue",
                "max_drones": "2",
            },
        },
        {
            "name": "dead_end1",
            "x": 0,
            "y": 1,
            "metadata": {
                "color": "red",
                "max_drones": "2",
            },
        },
        {
            "name": "dead_end2",
            "x": 0,
            "y": 2,
            "metadata": {
                "color": "red",
            },
        },
        {
            "name": "dead_end3",
            "x": 2,
            "y": -1,
            "metadata": {
                "color": "red",
            },
        },
        {
            "name": "trap_loop1",
            "x": 4,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "orange",
            },
        },
        {
            "name": "trap_loop2",
            "x": 4,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "orange",
            },
        },
        {
            "name": "bottleneck",
            "x": 5,
            "y": 1,
            "metadata": {
                "color": "yellow",
                "max_drones": "2",
            },
        },
        {
            "name": "final_stretch1",
            "x": 6,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
            },
        },
        {
            "name": "final_stretch2",
            "x": 6,
            "y": 1,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
            },
        },
        {
            "name": "final_stretch3",
            "x": 6,
            "y": 2,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
            },
        },
        {
            "name": "goal",
            "x": 7,
            "y": 1,
            "metadata": {
                "color": "green",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 8,
    "name": "Complex maze with multiple dead ends and loops",
    "difficulty": "Hard Level 1",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "maze_a1",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "maze_a1",
            "to_hub": "maze_a2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_a1",
            "to_hub": "maze_b1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_b1",
            "to_hub": "maze_b2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_b2",
            "to_hub": "maze_c2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_c2",
            "to_hub": "maze_a2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_c2",
            "to_hub": "bottleneck",
            "metadata": {
            },
        },
        {
            "from_hub": "start",
            "to_hub": "dead_end1",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "dead_end1",
            "to_hub": "dead_end2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_a2",
            "to_hub": "dead_end3",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_a2",
            "to_hub": "trap_loop1",
            "metadata": {
            },
        },
        {
            "from_hub": "trap_loop1",
            "to_hub": "trap_loop2",
            "metadata": {
            },
        },
        {
            "from_hub": "trap_loop2",
            "to_hub": "maze_c1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_b1",
            "to_hub": "maze_c1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_c1",
            "to_hub": "maze_b2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_b2",
            "to_hub": "maze_a2",
            "metadata": {
            },
        },
        {
            "from_hub": "bottleneck",
            "to_hub": "final_stretch1",
            "metadata": {
            },
        },
        {
            "from_hub": "bottleneck",
            "to_hub": "final_stretch2",
            "metadata": {
            },
        },
        {
            "from_hub": "bottleneck",
            "to_hub": "final_stretch3",
            "metadata": {
            },
        },
        {
            "from_hub": "final_stretch1",
            "to_hub": "goal",
            "metadata": {
            },
        },
        {
            "from_hub": "final_stretch2",
            "to_hub": "goal",
            "metadata": {
            },
        },
        {
            "from_hub": "final_stretch3",
            "to_hub": "goal",
            "metadata": {
            },
        },
    ],
}

MAP_01_THE_IMPOSSIBLE_DREAM: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "gate_hell1",
            "x": 2,
            "y": 0,
            "metadata": {
                "color": "red",
                "max_drones": "1",
            },
        },
        {
            "name": "gate_hell2",
            "x": 3,
            "y": 0,
            "metadata": {
                "color": "red",
                "max_drones": "1",
            },
        },
        {
            "name": "gate_hell3",
            "x": 4,
            "y": 0,
            "metadata": {
                "color": "red",
                "max_drones": "1",
            },
        },
        {
            "name": "gate_hell4",
            "x": 5,
            "y": 0,
            "metadata": {
                "color": "red",
                "max_drones": "1",
            },
        },
        {
            "name": "gate_hell5",
            "x": 6,
            "y": 0,
            "metadata": {
                "color": "red",
                "max_drones": "1",
            },
        },
        {
            "name": "maze_trap_a1",
            "x": 2,
            "y": 1,
            "metadata": {
                "color": "purple",
            },
        },
        {
            "name": "maze_trap_a2",
            "x": 3,
            "y": 1,
            "metadata": {
                "color": "purple",
            },
        },
        {
            "name": "maze_trap_a3",
            "x": 4,
            "y": 1,
            "metadata": {
                "color": "purple",
            },
        },
        {
            "name": "maze_dead_a",
            "x": 5,
            "y": 1,
            "metadata": {
                "color": "black",
            },
        },
        {
            "name": "maze_trap_b1",
            "x": 2,
            "y": -1,
            "metadata": {
                "color": "purple",
            },
        },
        {
            "name": "maze_trap_b2",
            "x": 3,
            "y": -1,
            "metadata": {
                "color": "purple",
            },
        },
        {
            "name": "maze_trap_b3",
            "x": 4,
            "y": -1,
            "metadata": {
                "color": "purple",
            },
        },
        {
            "name": "maze_dead_b",
            "x": 5,
            "y": -1,
            "metadata": {
                "color": "black",
            },
        },
        {
            "name": "maze_loop1",
            "x": 2,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
            },
        },
        {
            "name": "maze_loop2",
            "x": 3,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
            },
        },
        {
            "name": "maze_loop3",
            "x": 4,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
            },
        },
        {
            "name": "maze_loop4",
            "x": 5,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
            },
        },
        {
            "name": "maze_loop5",
            "x": 6,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
            },
        },
        {
            "name": "maze_loop6",
            "x": 6,
            "y": 1,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
            },
        },
        {
            "name": "micro_gate1",
            "x": 7,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "1",
            },
        },
        {
            "name": "micro_gate2",
            "x": 8,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "1",
            },
        },
        {
            "name": "micro_gate3",
            "x": 9,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "1",
            },
        },
        {
            "name": "overflow_hell1",
            "x": 7,
            "y": 1,
            "metadata": {
                "zone": "restricted",
                "color": "maroon",
                "max_drones": "2",
            },
        },
        {
            "name": "overflow_hell2",
            "x": 8,
            "y": 1,
            "metadata": {
                "zone": "restricted",
                "color": "maroon",
                "max_drones": "2",
            },
        },
        {
            "name": "overflow_hell3",
            "x": 9,
            "y": 1,
            "metadata": {
                "zone": "restricted",
                "color": "maroon",
                "max_drones": "2",
            },
        },
        {
            "name": "overflow_hell4",
            "x": 7,
            "y": -1,
            "metadata": {
                "zone": "restricted",
                "color": "maroon",
                "max_drones": "2",
            },
        },
        {
            "name": "overflow_hell5",
            "x": 8,
            "y": -1,
            "metadata": {
                "zone": "restricted",
                "color": "maroon",
                "max_drones": "2",
            },
        },
        {
            "name": "overflow_hell6",
            "x": 9,
            "y": -1,
            "metadata": {
                "zone": "restricted",
                "color": "maroon",
                "max_drones": "2",
            },
        },
        {
            "name": "false_hope1",
            "x": 10,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "gold",
                "max_drones": "3",
            },
        },
        {
            "name": "false_hope2",
            "x": 11,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "gold",
                "max_drones": "2",
            },
        },
        {
            "name": "false_hope3",
            "x": 12,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "gold",
                "max_drones": "1",
            },
        },
        {
            "name": "priority_trap1",
            "x": 10,
            "y": 1,
            "metadata": {
                "zone": "priority",
                "color": "gold",
            },
        },
        {
            "name": "priority_trap2",
            "x": 11,
            "y": 1,
            "metadata": {
                "zone": "priority",
                "color": "gold",
            },
        },
        {
            "name": "priority_dead",
            "x": 12,
            "y": 1,
            "metadata": {
                "color": "black",
            },
        },
        {
            "name": "priority_trap3",
            "x": 10,
            "y": -1,
            "metadata": {
                "zone": "priority",
                "color": "gold",
            },
        },
        {
            "name": "priority_trap4",
            "x": 11,
            "y": -1,
            "metadata": {
                "zone": "priority",
                "color": "gold",
            },
        },
        {
            "name": "priority_dead2",
            "x": 12,
            "y": -1,
            "metadata": {
                "color": "black",
            },
        },
        {
            "name": "conv_restricted1",
            "x": 13,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted2",
            "x": 14,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted3",
            "x": 15,
            "y": 2,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted4",
            "x": 13,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted5",
            "x": 14,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted6",
            "x": 15,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted7",
            "x": 13,
            "y": -2,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted8",
            "x": 14,
            "y": -2,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "conv_restricted9",
            "x": 15,
            "y": -2,
            "metadata": {
                "zone": "restricted",
                "color": "darkred",
                "max_drones": "1",
            },
        },
        {
            "name": "final_merge",
            "x": 16,
            "y": 0,
            "metadata": {
                "color": "violet",
                "max_drones": "5",
            },
        },
        {
            "name": "final_torture1",
            "x": 17,
            "y": 0,
            "metadata": {
                "color": "crimson",
                "max_drones": "2",
            },
        },
        {
            "name": "final_torture2",
            "x": 18,
            "y": 0,
            "metadata": {
                "color": "crimson",
                "max_drones": "1",
            },
        },
        {
            "name": "final_torture3",
            "x": 19,
            "y": 0,
            "metadata": {
                "color": "crimson",
                "max_drones": "1",
            },
        },
        {
            "name": "final_torture4",
            "x": 20,
            "y": 0,
            "metadata": {
                "color": "crimson",
                "max_drones": "1",
            },
        },
        {
            "name": "final_torture5",
            "x": 21,
            "y": 0,
            "metadata": {
                "color": "crimson",
                "max_drones": "1",
            },
        },
        {
            "name": "impossible_goal",
            "x": 23,
            "y": 0,
            "metadata": {
                "color": "rainbow",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 25,
    "name": "THE IMPOSSIBLE DREAM",
    "difficulty": "CHALLENGER LEVEL",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "gate_hell1",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate_hell1",
            "to_hub": "gate_hell2",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate_hell2",
            "to_hub": "gate_hell3",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate_hell3",
            "to_hub": "gate_hell4",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate_hell4",
            "to_hub": "gate_hell5",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate_hell1",
            "to_hub": "maze_trap_a1",
            "metadata": {
            },
        },
        {
            "from_hub": "gate_hell2",
            "to_hub": "maze_trap_b1",
            "metadata": {
            },
        },
        {
            "from_hub": "gate_hell3",
            "to_hub": "maze_loop1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_a1",
            "to_hub": "maze_trap_a2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_a2",
            "to_hub": "maze_trap_a3",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_a3",
            "to_hub": "maze_dead_a",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_b1",
            "to_hub": "maze_trap_b2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_b2",
            "to_hub": "maze_trap_b3",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_b3",
            "to_hub": "maze_dead_b",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop1",
            "to_hub": "maze_loop2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop2",
            "to_hub": "maze_loop3",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop3",
            "to_hub": "maze_loop4",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop4",
            "to_hub": "maze_loop5",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop5",
            "to_hub": "maze_loop6",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop6",
            "to_hub": "maze_loop1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_a2",
            "to_hub": "micro_gate1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap_b2",
            "to_hub": "micro_gate1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop3",
            "to_hub": "micro_gate2",
            "metadata": {
            },
        },
        {
            "from_hub": "gate_hell5",
            "to_hub": "micro_gate1",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate1",
            "to_hub": "micro_gate2",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate2",
            "to_hub": "micro_gate3",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate1",
            "to_hub": "overflow_hell1",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate2",
            "to_hub": "overflow_hell2",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate3",
            "to_hub": "overflow_hell3",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate1",
            "to_hub": "overflow_hell4",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate2",
            "to_hub": "overflow_hell5",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate3",
            "to_hub": "overflow_hell6",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell1",
            "to_hub": "overflow_hell2",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell2",
            "to_hub": "overflow_hell3",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell4",
            "to_hub": "overflow_hell5",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell5",
            "to_hub": "overflow_hell6",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell3",
            "to_hub": "false_hope1",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell6",
            "to_hub": "false_hope1",
            "metadata": {
            },
        },
        {
            "from_hub": "micro_gate3",
            "to_hub": "false_hope1",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope1",
            "to_hub": "false_hope2",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope2",
            "to_hub": "false_hope3",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope1",
            "to_hub": "priority_trap1",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope2",
            "to_hub": "priority_trap2",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope3",
            "to_hub": "priority_dead",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope1",
            "to_hub": "priority_trap3",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope2",
            "to_hub": "priority_trap4",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope3",
            "to_hub": "priority_dead2",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_trap1",
            "to_hub": "priority_trap2",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_trap3",
            "to_hub": "priority_trap4",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope3",
            "to_hub": "conv_restricted1",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope3",
            "to_hub": "conv_restricted4",
            "metadata": {
            },
        },
        {
            "from_hub": "false_hope3",
            "to_hub": "conv_restricted7",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted1",
            "to_hub": "conv_restricted2",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted2",
            "to_hub": "conv_restricted3",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted4",
            "to_hub": "conv_restricted5",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted5",
            "to_hub": "conv_restricted6",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted7",
            "to_hub": "conv_restricted8",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted8",
            "to_hub": "conv_restricted9",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted3",
            "to_hub": "final_merge",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted6",
            "to_hub": "final_merge",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted9",
            "to_hub": "final_merge",
            "metadata": {
            },
        },
        {
            "from_hub": "final_merge",
            "to_hub": "final_torture1",
            "metadata": {
            },
        },
        {
            "from_hub": "final_torture1",
            "to_hub": "final_torture2",
            "metadata": {
            },
        },
        {
            "from_hub": "final_torture2",
            "to_hub": "final_torture3",
            "metadata": {
            },
        },
        {
            "from_hub": "final_torture3",
            "to_hub": "final_torture4",
            "metadata": {
            },
        },
        {
            "from_hub": "final_torture4",
            "to_hub": "final_torture5",
            "metadata": {
            },
        },
        {
            "from_hub": "final_torture5",
            "to_hub": "impossible_goal",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell1",
            "to_hub": "conv_restricted1",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow_hell4",
            "to_hub": "conv_restricted7",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_trap1",
            "to_hub": "conv_restricted4",
            "metadata": {
            },
        },
    ],
}

MAP_02_CAPACITY_HELL: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": -1,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "gate1",
            "x": 1,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "1",
            },
        },
        {
            "name": "gate2",
            "x": 2,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "1",
            },
        },
        {
            "name": "gate3",
            "x": 3,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "1",
            },
        },
        {
            "name": "waiting_area1",
            "x": 1,
            "y": 1,
            "metadata": {
                "color": "blue",
                "max_drones": "4",
            },
        },
        {
            "name": "waiting_area2",
            "x": 2,
            "y": 1,
            "metadata": {
                "color": "blue",
                "max_drones": "4",
            },
        },
        {
            "name": "waiting_area3",
            "x": 3,
            "y": 1,
            "metadata": {
                "color": "blue",
                "max_drones": "4",
            },
        },
        {
            "name": "restricted_tunnel1",
            "x": 4,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "red",
                "max_drones": "2",
            },
        },
        {
            "name": "restricted_tunnel2",
            "x": 5,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "red",
                "max_drones": "2",
            },
        },
        {
            "name": "restricted_tunnel3",
            "x": 6,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "red",
                "max_drones": "2",
            },
        },
        {
            "name": "priority_bypass1",
            "x": 3,
            "y": 2,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
                "max_drones": "3",
            },
        },
        {
            "name": "priority_bypass2",
            "x": 4,
            "y": 2,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
                "max_drones": "3",
            },
        },
        {
            "name": "convergence",
            "x": 7,
            "y": 0,
            "metadata": {
                "color": "yellow",
                "max_drones": "6",
            },
        },
        {
            "name": "final_bottleneck",
            "x": 8,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "3",
            },
        },
        {
            "name": "goal",
            "x": 9,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 12,
    "name": "Extreme capacity constraints with timing challenges",
    "difficulty": "Hard Level 2",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "gate1",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "start",
            "to_hub": "gate2",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "start",
            "to_hub": "gate3",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate1",
            "to_hub": "gate2",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate2",
            "to_hub": "gate3",
            "metadata": {
                "max_link_capacity": "1",
            },
        },
        {
            "from_hub": "gate1",
            "to_hub": "waiting_area1",
            "metadata": {
            },
        },
        {
            "from_hub": "gate2",
            "to_hub": "waiting_area2",
            "metadata": {
            },
        },
        {
            "from_hub": "gate3",
            "to_hub": "waiting_area3",
            "metadata": {
            },
        },
        {
            "from_hub": "waiting_area1",
            "to_hub": "waiting_area2",
            "metadata": {
            },
        },
        {
            "from_hub": "waiting_area2",
            "to_hub": "waiting_area3",
            "metadata": {
            },
        },
        {
            "from_hub": "gate3",
            "to_hub": "restricted_tunnel1",
            "metadata": {
            },
        },
        {
            "from_hub": "restricted_tunnel1",
            "to_hub": "restricted_tunnel2",
            "metadata": {
            },
        },
        {
            "from_hub": "restricted_tunnel2",
            "to_hub": "restricted_tunnel3",
            "metadata": {
            },
        },
        {
            "from_hub": "restricted_tunnel3",
            "to_hub": "convergence",
            "metadata": {
            },
        },
        {
            "from_hub": "waiting_area1",
            "to_hub": "priority_bypass1",
            "metadata": {
            },
        },
        {
            "from_hub": "waiting_area2",
            "to_hub": "priority_bypass2",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_bypass1",
            "to_hub": "priority_bypass2",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_bypass2",
            "to_hub": "convergence",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "convergence",
            "to_hub": "final_bottleneck",
            "metadata": {
                "max_link_capacity": "3",
            },
        },
        {
            "from_hub": "final_bottleneck",
            "to_hub": "goal",
            "metadata": {
            },
        },
        {
            "from_hub": "waiting_area3",
            "to_hub": "convergence",
            "metadata": {
            },
        },
    ],
}

MAP_02_CIRCULAR_LOOP: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "loop_a",
            "x": 1,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "2",
            },
        },
        {
            "name": "loop_b",
            "x": 2,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "2",
            },
        },
        {
            "name": "loop_c",
            "x": 2,
            "y": 1,
            "metadata": {
                "color": "orange",
                "max_drones": "2",
            },
        },
        {
            "name": "loop_d",
            "x": 1,
            "y": 1,
            "metadata": {
                "color": "orange",
                "max_drones": "2",
            },
        },
        {
            "name": "exit_point",
            "x": 3,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "blue",
            },
        },
        {
            "name": "goal",
            "x": 4,
            "y": 0,
            "metadata": {
                "color": "red",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 6,
    "name": "Circular loop with restricted zones",
    "difficulty": "Medium Level 2",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "loop_a",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "loop_a",
            "to_hub": "loop_b",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "loop_b",
            "to_hub": "loop_c",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "loop_c",
            "to_hub": "loop_d",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "loop_d",
            "to_hub": "loop_a",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "loop_b",
            "to_hub": "exit_point",
            "metadata": {
            },
        },
        {
            "from_hub": "exit_point",
            "to_hub": "goal",
            "metadata": {
            },
        },
    ],
}

MAP_02_SIMPLE_FORK: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "junction",
            "x": 1,
            "y": 0,
            "metadata": {
                "color": "yellow",
                "max_drones": "2",
            },
        },
        {
            "name": "path_a",
            "x": 2,
            "y": 1,
            "metadata": {
                "color": "blue",
            },
        },
        {
            "name": "path_b",
            "x": 2,
            "y": -1,
            "metadata": {
                "color": "blue",
            },
        },
        {
            "name": "goal",
            "x": 3,
            "y": 0,
            "metadata": {
                "color": "red",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 4,
    "name": "Simple fork with two paths",
    "difficulty": "Easy Level 2",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "junction",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "junction",
            "to_hub": "path_a",
            "metadata": {
            },
        },
        {
            "from_hub": "junction",
            "to_hub": "path_b",
            "metadata": {
            },
        },
        {
            "from_hub": "path_a",
            "to_hub": "goal",
            "metadata": {
            },
        },
        {
            "from_hub": "path_b",
            "to_hub": "goal",
            "metadata": {
            },
        },
    ],
}

MAP_03_BASIC_CAPACITY: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "bottleneck",
            "x": 1,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "2",
            },
        },
        {
            "name": "wide_area",
            "x": 2,
            "y": 0,
            "metadata": {
                "color": "blue",
                "max_drones": "3",
            },
        },
        {
            "name": "goal",
            "x": 3,
            "y": 0,
            "metadata": {
                "color": "red",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 4,
    "name": "Basic capacity management",
    "difficulty": "Easy Level 3",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "bottleneck",
            "metadata": {
                "max_link_capacity": "4",
            },
        },
        {
            "from_hub": "bottleneck",
            "to_hub": "wide_area",
            "metadata": {
                "max_link_capacity": "4",
            },
        },
        {
            "from_hub": "wide_area",
            "to_hub": "goal",
            "metadata": {
                "max_link_capacity": "4",
            },
        },
    ],
}

MAP_03_PRIORITY_PUZZLE: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "slow_path1",
            "x": 1,
            "y": -1,
            "metadata": {
                "zone": "restricted",
                "color": "red",
            },
        },
        {
            "name": "slow_path2",
            "x": 2,
            "y": -1,
            "metadata": {
                "color": "red",
            },
        },
        {
            "name": "fast_junction",
            "x": 1,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "blue",
                "max_drones": "2",
            },
        },
        {
            "name": "fast_path",
            "x": 2,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "blue",
            },
        },
        {
            "name": "merge_point",
            "x": 3,
            "y": 0,
            "metadata": {
                "color": "yellow",
                "max_drones": "3",
            },
        },
        {
            "name": "goal",
            "x": 4,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 5,
    "name": "Priority zones create optimal path challenges",
    "difficulty": "Medium Level 3",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "slow_path1",
            "metadata": {
            },
        },
        {
            "from_hub": "start",
            "to_hub": "fast_junction",
            "metadata": {
            },
        },
        {
            "from_hub": "slow_path1",
            "to_hub": "slow_path2",
            "metadata": {
            },
        },
        {
            "from_hub": "slow_path2",
            "to_hub": "merge_point",
            "metadata": {
            },
        },
        {
            "from_hub": "fast_junction",
            "to_hub": "fast_path",
            "metadata": {
            },
        },
        {
            "from_hub": "fast_path",
            "to_hub": "merge_point",
            "metadata": {
            },
        },
        {
            "from_hub": "merge_point",
            "to_hub": "goal",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
    ],
}

MAP_03_ULTIMATE_CHALLENGE: dict[str, Any] = {
    "hub_list": [
        {
            "name": "start",
            "x": 0,
            "y": 0,
            "metadata": {
                "color": "green",
                "hub_type": "start",
            },
        },
        {
            "name": "dist_gate1",
            "x": 1,
            "y": -1,
            "metadata": {
                "color": "orange",
            },
        },
        {
            "name": "dist_gate2",
            "x": 1,
            "y": 1,
            "metadata": {
                "color": "orange",
            },
        },
        {
            "name": "dist_gate3",
            "x": 1,
            "y": 0,
            "metadata": {
                "color": "orange",
            },
        },
        {
            "name": "maze_trap1",
            "x": 1,
            "y": 2,
            "metadata": {
                "color": "red",
            },
        },
        {
            "name": "maze_trap2",
            "x": 2,
            "y": 2,
            "metadata": {
                "color": "red",
                "max_drones": "3",
            },
        },
        {
            "name": "maze_loop1",
            "x": 2,
            "y": 1,
            "metadata": {
                "color": "purple",
                "max_drones": "3",
            },
        },
        {
            "name": "maze_loop2",
            "x": 3,
            "y": 1,
            "metadata": {
                "color": "purple",
                "max_drones": "3",
            },
        },
        {
            "name": "maze_loop3",
            "x": 4,
            "y": 1,
            "metadata": {
                "color": "purple",
                "max_drones": "3",
            },
        },
        {
            "name": "maze_loop4",
            "x": 3,
            "y": 2,
            "metadata": {
                "color": "purple",
                "max_drones": "3",
            },
        },
        {
            "name": "maze_correct",
            "x": 2,
            "y": 0,
            "metadata": {
                "color": "blue",
                "max_drones": "3",
            },
        },
        {
            "name": "bottleneck1",
            "x": 3,
            "y": 0,
            "metadata": {
                "color": "yellow",
                "max_drones": "2",
            },
        },
        {
            "name": "bottleneck2",
            "x": 4,
            "y": 0,
            "metadata": {
                "color": "yellow",
                "max_drones": "1",
            },
        },
        {
            "name": "overflow1",
            "x": 3,
            "y": -1,
            "metadata": {
                "zone": "restricted",
                "color": "orange",
                "max_drones": "3",
            },
        },
        {
            "name": "overflow2",
            "x": 4,
            "y": -1,
            "metadata": {
                "zone": "restricted",
                "color": "orange",
                "max_drones": "3",
            },
        },
        {
            "name": "priority_hub",
            "x": 5,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
                "max_drones": "4",
            },
        },
        {
            "name": "priority_trap1",
            "x": 5,
            "y": 1,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
            },
        },
        {
            "name": "priority_trap2",
            "x": 6,
            "y": 1,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
            },
        },
        {
            "name": "priority_dead_end",
            "x": 6,
            "y": 2,
            "metadata": {
                "color": "red",
            },
        },
        {
            "name": "priority_correct",
            "x": 6,
            "y": 0,
            "metadata": {
                "zone": "priority",
                "color": "cyan",
                "max_drones": "3",
            },
        },
        {
            "name": "conv_restricted1",
            "x": 7,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
                "max_drones": "2",
            },
        },
        {
            "name": "conv_restricted2",
            "x": 8,
            "y": 0,
            "metadata": {
                "zone": "restricted",
                "color": "brown",
                "max_drones": "2",
            },
        },
        {
            "name": "conv_normal1",
            "x": 7,
            "y": -1,
            "metadata": {
                "color": "blue",
                "max_drones": "3",
            },
        },
        {
            "name": "conv_normal2",
            "x": 8,
            "y": -1,
            "metadata": {
                "color": "blue",
                "max_drones": "3",
            },
        },
        {
            "name": "conv_priority1",
            "x": 7,
            "y": 1,
            "metadata": {
                "zone": "priority",
                "color": "lime",
                "max_drones": "2",
            },
        },
        {
            "name": "conv_priority2",
            "x": 8,
            "y": 1,
            "metadata": {
                "zone": "priority",
                "color": "lime",
                "max_drones": "2",
            },
        },
        {
            "name": "final_merge",
            "x": 9,
            "y": 0,
            "metadata": {
                "color": "magenta",
                "max_drones": "8",
            },
        },
        {
            "name": "final_gate1",
            "x": 10,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "3",
            },
        },
        {
            "name": "final_gate2",
            "x": 11,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "2",
            },
        },
        {
            "name": "final_gate3",
            "x": 12,
            "y": 0,
            "metadata": {
                "color": "orange",
                "max_drones": "1",
            },
        },
        {
            "name": "goal",
            "x": 13,
            "y": 0,
            "metadata": {
                "color": "gold",
                "hub_type": "end",
            },
        },
    ],
    "nb_drones": 15,
    "name": "THE ULTIMATE CHALLENGE - All tricks combined",
    "difficulty": "Hard Level 3",
    "connections": [
        {
            "from_hub": "start",
            "to_hub": "dist_gate1",
            "metadata": {
            },
        },
        {
            "from_hub": "start",
            "to_hub": "dist_gate2",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "start",
            "to_hub": "dist_gate3",
            "metadata": {
            },
        },
        {
            "from_hub": "dist_gate1",
            "to_hub": "maze_correct",
            "metadata": {
            },
        },
        {
            "from_hub": "dist_gate2",
            "to_hub": "maze_trap1",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "dist_gate3",
            "to_hub": "maze_loop1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_trap1",
            "to_hub": "maze_trap2",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "maze_loop1",
            "to_hub": "maze_loop2",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop2",
            "to_hub": "maze_loop3",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop3",
            "to_hub": "maze_loop4",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop4",
            "to_hub": "maze_loop1",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_loop2",
            "to_hub": "maze_correct",
            "metadata": {
            },
        },
        {
            "from_hub": "maze_correct",
            "to_hub": "bottleneck1",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "bottleneck1",
            "to_hub": "bottleneck2",
            "metadata": {
            },
        },
        {
            "from_hub": "bottleneck1",
            "to_hub": "overflow1",
            "metadata": {
            },
        },
        {
            "from_hub": "overflow1",
            "to_hub": "overflow2",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "overflow2",
            "to_hub": "bottleneck2",
            "metadata": {
            },
        },
        {
            "from_hub": "bottleneck2",
            "to_hub": "priority_hub",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_hub",
            "to_hub": "priority_trap1",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_hub",
            "to_hub": "priority_correct",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_trap1",
            "to_hub": "priority_trap2",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_trap2",
            "to_hub": "priority_dead_end",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_correct",
            "to_hub": "conv_restricted1",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_correct",
            "to_hub": "conv_normal1",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_correct",
            "to_hub": "conv_priority1",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_restricted1",
            "to_hub": "conv_restricted2",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_normal1",
            "to_hub": "conv_normal2",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_priority1",
            "to_hub": "conv_priority2",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "conv_restricted2",
            "to_hub": "final_merge",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_normal2",
            "to_hub": "final_merge",
            "metadata": {
            },
        },
        {
            "from_hub": "conv_priority2",
            "to_hub": "final_merge",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "final_merge",
            "to_hub": "final_gate1",
            "metadata": {
                "max_link_capacity": "3",
            },
        },
        {
            "from_hub": "final_gate1",
            "to_hub": "final_gate2",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "final_gate2",
            "to_hub": "final_gate3",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "final_gate3",
            "to_hub": "goal",
            "metadata": {
                "max_link_capacity": "2",
            },
        },
        {
            "from_hub": "overflow2",
            "to_hub": "conv_normal1",
            "metadata": {
            },
        },
        {
            "from_hub": "priority_hub",
            "to_hub": "conv_priority1",
            "metadata": {
            },
        },
    ],
}

# ALL_MAPS.get("<Map_name>")

ALL_MAPS: dict[str, dict[str, Any]] = {
    map_["name"]: map_
    for map_ in [
        MAP_01_DEAD_END_TRAP,
        MAP_01_MAZE_NIGHTMARE,
        MAP_01_THE_IMPOSSIBLE_DREAM,
        MAP_02_CAPACITY_HELL,
        MAP_02_CIRCULAR_LOOP,
        MAP_02_SIMPLE_FORK,
        MAP_03_BASIC_CAPACITY,
        MAP_03_PRIORITY_PUZZLE,
        MAP_03_ULTIMATE_CHALLENGE,
    ]
}

# Short filenames matching the benchmark map names, keyed by each map's
# full "name" field, so generated map files stay recognizable during
# evaluation instead of using the long descriptive names.
MAP_NAMES: dict[str, str] = {
    "Simple Linear Path": "linear_path",
    "Simple fork with two paths": "simple_fork",
    "Basic capacity management": "basic_capacity",
    "Dead end trap - drones might get stuck": "dead_end_trap",
    "Circular loop with restricted zones": "circular_loop",
    "Priority zones create optimal path challenges": "priority_puzzle",
    "Complex maze with multiple dead ends and loops": "maze_nightmare",
    "Extreme capacity constraints with timing challenges": "capacity_hell",
    "THE ULTIMATE CHALLENGE - All tricks combined": "ultimate_challenge",
    "THE IMPOSSIBLE DREAM": "the_impossible_dream",
}
