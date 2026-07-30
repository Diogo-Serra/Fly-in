# Renderer class for Fly-in
from .map import Map
from math import hypot
from pathlib import Path
from .pathfinder import Pathfinder
from .resources import constants as RC

try:
    import pygame
except Exception as error:
    print(error)
    exit(1)


class Renderer:

    @staticmethod
    def _resolve_color(name: str) -> tuple[int, int, int]:
        return RC.COLOR_NAMES.get(name.upper(), (255, 255, 255))

    def __init__(self, nav_map: Map, pathfinder: Pathfinder) -> None:
        self.nav_map = nav_map
        self._pf = pathfinder
        self._tick: int = 0
        self._playing: bool = False
        self._last_tick_ms: int = 0
        self._tick_delay_ms: int = RC.TICK_DELAY_MS
        xs = [h.x for h in nav_map.hub_list]
        ys = [h.y for h in nav_map.hub_list]
        self._min_x, self._max_x = min(xs), max(xs)
        self._min_y, self._max_y = min(ys), max(ys)
        hx = {h.name: h.x for h in nav_map.hub_list}
        hy = {h.name: h.y for h in nav_map.hub_list}
        self._label_above: set[str] = set()
        for c in nav_map.connections:
            if hx.get(c.from_hub) == hx.get(c.to_hub):
                fy, ty = hy.get(c.from_hub, 0), hy.get(c.to_hub, 0)
                if ty < fy:
                    self._label_above.add(c.from_hub)
                if fy < ty:
                    self._label_above.add(c.to_hub)

        pygame.init()

        _info = pygame.display.Info()
        self._win_w, self._win_h = _info.current_w, _info.current_h
        self._panel_h = max(80, self._win_h // 10)
        self._map_h = self._win_h - self._panel_h
        self._margin = max(60, min(self._win_w, self._win_h) // 14)
        self._scale = self._compute_scale()
        _cw = (self._max_x - self._min_x) * self._scale
        self._content_h = (self._max_y - self._min_y) * self._scale
        _aw = self._win_w - self._margin * 2
        _ah = self._map_h - self._margin * 2
        self._ox = self._margin + (_aw - _cw) / 2
        self._oy = self._panel_h + self._margin + (_ah - self._content_h) / 2
        _r = int(min(RC.HUB_RADIUS, self._scale * RC.HUB_SCALE_RATIO))
        self._hub_radius = max(RC.MIN_HUB_RADIUS, _r)
        self._drone_badge_r = max(
            3, int(RC.DRONE_BADGE_R * self._hub_radius / RC.HUB_RADIUS))
        self._show_labels = True
        self._show_solution: bool = False
        self._solution_lines: list[str] | None = None
        self._anim_progress = 0.0
        self._single_step = False
        self._screen = pygame.display.set_mode(
            (self._win_w, self._win_h), pygame.FULLSCREEN)
        pygame.display.set_caption("Fly-in - Navigation")
        self._font_sm = pygame.font.SysFont(None, 18)
        self._font_hub_inner = pygame.font.SysFont(None, 16)
        self._font_panel = pygame.font.SysFont(None, 26)
        self._title_surf = self._font_panel.render(
            f"{self.nav_map.name}  ·  {self.nav_map.difficulty}"
            f"  ·  {self.nav_map.nb_drones} drones",
            True, (255, 255, 255)
        )
        self._opts_surf = self._font_sm.render(
            "P · play/pause    <- -> · step    R · reset"
            "    L · labels   S · solution   ESC · quit",
            True, (160, 160, 180)
        )
        self._clock = pygame.time.Clock()

    def _compute_scale(self) -> float:
        sx, sy = self._max_x - self._min_x, self._max_y - self._min_y
        aw = self._win_w - self._margin * 2
        ah = self._map_h - self._margin * 2
        if sx > 0 and sy > 0:
            scale = min(aw / sx, ah / sy)
        elif sx > 0:
            scale = aw / sx
        elif sy > 0:
            scale = ah / sy
        else:
            scale = RC.MAX_SCALE
        return min(scale, RC.MAX_SCALE)

    def _to_screen(self, x: int, y: int) -> tuple[int, int]:
        sx = int(self._ox + (x - self._min_x) * self._scale)
        sy = int(self._oy + self._content_h - (y - self._min_y) * self._scale)
        return sx, sy

    def _advance_tick(self) -> None:
        if self._tick < self._pf.total_ticks - 1:
            self._tick += 1
        else:
            self._playing = False

    def run(self) -> None:
        running = True
        self._last_tick_ms = pygame.time.get_ticks()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_l:
                        self._show_labels = not self._show_labels
                    elif event.key == pygame.K_p:
                        self._playing = not self._playing
                        self._anim_progress = 0.0
                        dw = (
                            int(self._tick_delay_ms * RC.DWELL_RATIO)
                            if self._playing else 0)
                        self._last_tick_ms = pygame.time.get_ticks() - dw
                    elif event.key == pygame.K_RIGHT:
                        if not self._playing and not self._single_step:
                            self._single_step = True
                            self._anim_progress = 0.0
                            self._last_tick_ms = pygame.time.get_ticks()
                    elif event.key == pygame.K_s:
                        self._toggle_solution()
                    elif event.key == pygame.K_LEFT:
                        if not self._playing and not self._single_step:
                            self._tick -= 1 if self._tick > 0 else 0
                            self._anim_progress = 0.0
                    elif event.key == pygame.K_r:
                        self._tick = 0
                        self._playing = False
                        self._single_step = False
                        self._anim_progress = 0.0

            now = pygame.time.get_ticks()
            elapsed = now - self._last_tick_ms
            if self._single_step:
                self._anim_progress = min(1.0, elapsed / RC.STEP_ANIM_MS)
                if elapsed >= RC.STEP_ANIM_MS:
                    self._advance_tick()
                    self._last_tick_ms = now
                    self._anim_progress = 0.0
                    self._single_step = False
            elif self._playing:
                if elapsed >= self._tick_delay_ms:
                    self._advance_tick()
                    self._last_tick_ms = now
                    self._anim_progress = 0.0
                else:
                    dwell = self._tick_delay_ms * RC.DWELL_RATIO
                    transit = self._tick_delay_ms - dwell
                    if elapsed > dwell:
                        self._anim_progress = (elapsed - dwell) / transit
                    else:
                        self._anim_progress = 0.0

            self._screen.fill(RC.BG_COLOR)
            self._draw_connections()
            self._draw_hubs()
            self._draw_drones()
            self._draw_panel()
            self._draw_map_info()
            if self._show_solution:
                self._draw_solution_overlay()
            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()

    def _blit_centered(self, surf: pygame.Surface, cx: int, cy: int) -> None:
        rect = surf.get_rect(center=(cx, cy))
        self._screen.blit(surf, rect)

    def _draw_bg_box(
        self, x: int, y: int, w: int, h: int,
        fill: tuple, border: tuple | None = None, border_w: int = 1
    ) -> None:
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill(fill)
        if border is not None:
            pygame.draw.rect(bg, border, bg.get_rect(), border_w)
        self._screen.blit(bg, (x, y))

    def _draw_connections(self) -> None:
        pos = {h.name: self._to_screen(h.x, h.y)
               for h in self.nav_map.hub_list}
        for conn in self.nav_map.connections:
            a, b = pos.get(conn.from_hub), pos.get(conn.to_hub)
            if not a or not b:
                continue
            pygame.draw.line(self._screen, (120, 120, 140), a, b, 2)
            cap = conn.metadata.get('max_link_capacity', '')
            if not cap or not self._show_labels:
                continue
            ln = hypot(b[0]-a[0], b[1]-a[1]) or 1
            px, py = -(b[1]-a[1]) / ln, (b[0]-a[0]) / ln
            lx = (a[0]+b[0])//2 + int(px*16)
            ly = (a[1]+b[1])//2 + int(py*16)
            label = self._font_sm.render(f"cap:{cap}", True, (200, 200, 220))
            lw, lh = label.get_size()
            self._draw_bg_box(
                lx - lw // 2 - 3, ly - lh // 2 - 3, lw + 6, lh + 6,
                (10, 10, 25, 200))
            self._blit_centered(label, lx, ly)

    def _draw_hubs(self) -> None:
        r = self._hub_radius
        border = max(1, r // 10)
        for hub in self.nav_map.hub_list:
            sx, sy = self._to_screen(hub.x, hub.y)
            color = self._resolve_color(hub.metadata.get('color', 'white'))
            pygame.draw.circle(self._screen, color, (sx, sy), r)
            pygame.draw.circle(
                self._screen, (255, 255, 255), (sx, sy), r, border)
            if not self._show_labels:
                continue

            if r >= 14:
                cap = hub.metadata.get('max_drones', '')
                coord_txt = f"({hub.x},{hub.y})"
                coord_surf = self._font_hub_inner.render(
                    coord_txt, True, (0, 0, 0))
                if cap:
                    max_surf = self._font_hub_inner.render(
                        f"max:{cap}", True, (0, 0, 0))
                    self._blit_centered(coord_surf, sx, sy - 8)
                    self._blit_centered(max_surf, sx, sy + 8)
                else:
                    self._blit_centered(coord_surf, sx, sy)
            if r >= 8:
                name_surf = self._font_sm.render(
                    hub.name, True, (255, 255, 255))
                if hub.name in self._label_above:
                    name_rect = name_surf.get_rect(
                        midbottom=(sx, sy - r - 4))
                else:
                    name_rect = name_surf.get_rect(
                        midtop=(sx, sy + r + 4))
                self._screen.blit(name_surf, name_rect)

    def _draw_drones(self) -> None:
        if not self._pf.ticks:
            return
        cur = self._pf.ticks[self._tick]
        has_next = self._tick + 1 < len(self._pf.ticks)
        nxt = self._pf.ticks[self._tick + 1] if has_next else None
        prog = self._anim_progress if has_next else 0.0
        hub_by_name = {h.name: h for h in self.nav_map.hub_list}

        def _badge(name: str, n: int) -> None:
            hub = hub_by_name.get(name)
            if not hub:
                return
            sx, sy = self._to_screen(hub.x, hub.y)
            bx = sx + int(self._hub_radius * 0.72)
            by = sy - int(self._hub_radius * 0.72)
            r = self._drone_badge_r
            pygame.draw.circle(self._screen, (230, 140, 40), (bx, by), r)
            pygame.draw.circle(self._screen, (255, 255, 255), (bx, by), r, 1)
            surf = self._font_hub_inner.render(str(n), True, (255, 255, 255))
            self._blit_centered(surf, bx, by)

        if prog > 0.0 and nxt is not None:
            at_rest: dict[str, int] = {}
            for c, nxt_name in zip(cur, nxt):
                if c == nxt_name:
                    at_rest[c] = at_rest.get(c, 0) + 1
                else:
                    ha = hub_by_name.get(c)
                    hb = hub_by_name.get(nxt_name)
                    if ha and hb:
                        ax, ay = self._to_screen(ha.x, ha.y)
                        bx, by = self._to_screen(hb.x, hb.y)
                        dx = int(ax + (bx - ax) * prog)
                        dy = int(ay + (by - ay) * prog)
                        r = max(3, self._drone_badge_r - 1)
                        pygame.draw.circle(
                            self._screen, (230, 140, 40), (dx, dy), r)
            for name, n in at_rest.items():
                _badge(name, n)
        else:
            count: dict[str, int] = {}
            for name in cur:
                count[name] = count.get(name, 0) + 1
            for name, n in count.items():
                _badge(name, n)

    def _draw_map_info(self) -> None:
        pad = 10
        line_gap = 4
        margin = 14
        lines = [
            self.nav_map.name,
            f"Difficulty : {self.nav_map.difficulty}",
            f"Drones     : {self.nav_map.nb_drones}",
            f"Hubs       : {len(self.nav_map.hub_list)}",
            f"Links      : {len(self.nav_map.connections)}",
        ]
        surfs = [self._font_sm.render(ln, True, (210, 210, 235))
                 for ln in lines]
        box_w = max(s.get_width() for s in surfs) + pad * 2
        line_h = surfs[0].get_height() + line_gap
        box_h = line_h * len(surfs) + pad * 2 - line_gap
        bx = self._win_w - box_w - margin
        by = self._panel_h + margin
        self._draw_bg_box(
            bx, by, box_w, box_h, (10, 10, 28, 210), (90, 90, 140, 200))
        for i, surf in enumerate(surfs):
            self._screen.blit(surf, (bx + pad, by + pad + i * line_h))

    def _draw_solution_overlay(self) -> None:
        lines = self._load_solution_lines()
        pad, line_gap = 12, 3
        box_w, box_h = int(self._win_w * 0.5), int(self._win_h * 0.6)
        bx = (self._win_w - box_w) // 2
        by = (self._win_h - box_h) // 2

        self._draw_bg_box(
            bx, by, box_w, box_h, RC.SOLUTION_BG, RC.SOLUTION_BORDER, 2)

        title = self._font_panel.render(
            "Solution (S to close)", True, (255, 255, 255))
        self._screen.blit(title, (bx + pad, by + pad))

        content_top = by + pad + title.get_height() + line_gap
        content_h = by + box_h - pad - content_top
        available_w = box_w - pad * 2
        line_h = self._font_sm.get_height() + line_gap
        max_lines = max(1, content_h // line_h)

        labeled = [f"T{i+1}: {line}" for i, line in enumerate(lines)]
        too_tall = len(labeled) > max_lines
        too_wide = any(
            self._font_sm.size(text)[0] > available_w for text in labeled
        )

        if too_tall or too_wide:
            name = self.nav_map.name.replace(' ', '_').lower()
            msg_lines = [
                "Solution too large to display here.",
                f"Check the full file at: solution/{name}.txt",
            ]
            y = content_top + (content_h - len(msg_lines) * line_h) // 2
            for msg in msg_lines:
                surf = self._font_sm.render(msg, True, RC.SOLUTION_TEXT)
                self._blit_centered(
                    surf, bx + box_w // 2, y + surf.get_height() // 2)
                y += line_h
            return

        y = content_top
        for text in labeled:
            surf = self._font_sm.render(text, True, RC.SOLUTION_TEXT)
            self._screen.blit(surf, (bx + pad, y))
            y += line_h

    def _load_solution_lines(self) -> list[str]:
        if self._solution_lines is not None:
            return self._solution_lines
        root = Path(__file__).parent.parent.parent
        name = self.nav_map.name.replace(' ', '_').lower()
        path = root / "solution" / f"{name}.txt"
        if path.exists():
            self._solution_lines = path.read_text().splitlines()
        else:
            self._solution_lines = ["No solution file found."]
        return self._solution_lines

    def _toggle_solution(self) -> None:
        self._show_solution = not self._show_solution
        if self._show_solution:
            self._load_solution_lines()

    def _draw_panel(self) -> None:
        pygame.draw.rect(
            self._screen, (10, 10, 20), pygame.Rect(
                0, 0, self._win_w, self._panel_h))
        pygame.draw.line(
            self._screen, (80, 80, 100), (0, self._panel_h), (
                self._win_w, self._panel_h), 1)
        self._blit_centered(
            self._title_surf, self._win_w // 2, self._panel_h // 4)
        state = "PLAYING" if self._playing else "PAUSED"
        total = self._pf.total_ticks
        flow = self._pf.flow_reached
        tick_txt = (f"{state}  |  Turn {self._tick + 1} / {total}"
                    f"  |  Flow {flow} / {self.nav_map.nb_drones}")
        tick_col = (100, 220, 140) if self._playing else (220, 180, 80)
        tick_surf = self._font_sm.render(tick_txt, True, tick_col)
        ty = self._panel_h * 3 // 4 - tick_surf.get_height() // 2
        self._screen.blit(tick_surf, (14, ty))
        self._blit_centered(
            self._opts_surf, self._win_w // 2, self._panel_h * 3 // 4)
