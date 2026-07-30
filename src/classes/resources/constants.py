# Constants for Fly-in

# Hub geometry
HUB_RADIUS = 38
MAX_SCALE = 220
MIN_HUB_RADIUS = 5
DRONE_BADGE_R = 13
HUB_SCALE_RATIO = 0.38

# Animation timing (milliseconds)
DWELL_RATIO = 0.55
STEP_ANIM_MS = 450
TICK_DELAY_MS = 2000

# Background color
BG_COLOR = (18, 18, 38)

# Solution overlay colors
SOLUTION_BG = (12, 12, 26, 235)
SOLUTION_TEXT = (220, 220, 240)
SOLUTION_BORDER = (120, 120, 170)

# Named hub colours
COLOR_NAMES: dict[str, tuple[int, int, int]] = {
    "WHITE":     (255, 255, 255),
    "RED":       (220,  50,  50),
    "GREEN":     (50,  200,  80),
    "BLUE":      (60,  120, 220),
    "YELLOW":    (230, 210,  50),
    "CYAN":      (50,  210, 210),
    "MAGENTA":   (200,  60, 200),
    "ORANGE":    (230, 140,  40),
    "GRAY":      (140, 140, 140),
    "PURPLE":    (150,  60, 200),
    "PINK":      (230, 120, 160),
    "TEAL":      (40,  180, 160),
    "SKYBLUE":   (100, 180, 240),
    "STEELBLUE": (70,  130, 180),
    "NAVY":      (30,   60, 120),
    "BROWN":     (139,  90,  43),
    "LIME":      (130, 210,  50),
    "GOLD":      (212, 175,  55),
}
