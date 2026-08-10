# Renderer class for Fly-in
from .map import Hub, Map
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
        if not name:
            return RC.NO_COLOR
        return RC.COLOR_NAMES.get(name.upper(), RC.NO_COLOR)

    def _badge_letter(self, hub: Hub) -> str | None:
        return (
            RC.ZONE_BADGE.get(hub.hub_type)
            or RC.ZONE_BADGE.get(hub.zone)
        )

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

        pygame.init()

        self._win_w, self._win_h = RC.WINDOW_W, RC.WINDOW_H
        self._panel_h = max(80, self._win_h // 10)
        self._margin = 60

        self._font_sm = pygame.font.SysFont(None, 18)
        self._font_hub_inner = pygame.font.SysFont(None, 16)
        self._font_panel = pygame.font.SysFont(None, 26)

        self._info_lines = [
            self.nav_map.name,
            f"Difficulty : {self.nav_map.difficulty}",
            f"Drones     : {self.nav_map.nb_drones}",
            f"Hubs       : {len(self.nav_map.hub_list)}",
            f"Links      : {len(self.nav_map.connections)}",
        ]
        self._info_surfs, self._info_box_w, self._info_box_h = (
            self._measure_lines(self._info_lines))

        self._legend_lines = [
            "Legend",
            "S / E : start / end hub",
            "X : blocked   R : restricted (+1 tick)",
            "P : priority (routed first)",
            "Number in hub : capacity (max drones)",
            "Number on line : link capacity",
            "Hover a hub with the mouse for details",
        ]
        self._legend_surfs, self._legend_box_w, self._legend_box_h = (
            self._measure_lines(self._legend_lines))

        self._recompute_layout()
        self._show_labels = True
        self._show_solution: bool = False
        self._show_info: bool = False
        self._show_legend: bool = False
        self._info_btn = pygame.Rect(0, 0, 0, 0)
        self._legend_btn = pygame.Rect(0, 0, 0, 0)
        self._solution_lines: list[str] | None = None
        self._anim_progress = 0.0
        self._single_step = False
        self._screen = pygame.display.set_mode(
            (self._win_w, self._win_h), pygame.RESIZABLE)
        pygame.display.set_caption("Fly-in - Navigation")
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

    # Layout and scale

    def _measure_lines(
        self, lines: list[str], color: tuple[int, int, int] = (210, 210, 235)
    ) -> tuple[list[pygame.Surface], int, int]:
        pad, line_gap = 10, 4
        surfs = [self._font_sm.render(ln, True, color) for ln in lines]
        box_w = max(s.get_width() for s in surfs) + pad * 2
        line_h = surfs[0].get_height() + line_gap
        box_h = line_h * len(surfs) + pad * 2 - line_gap
        return surfs, box_w, box_h

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

    def _apply_scale(self) -> None:
        _r = int(min(RC.HUB_RADIUS, self._scale * RC.HUB_SCALE_RATIO))
        self._hub_radius = max(RC.MIN_HUB_RADIUS, _r)
        self._drone_badge_r = max(
            12, int(RC.DRONE_BADGE_R * self._hub_radius / RC.HUB_RADIUS))
        self._content_w = (self._max_x - self._min_x) * self._scale
        self._content_h = (self._max_y - self._min_y) * self._scale
        aw = self._win_w - self._margin * 2
        ah = self._map_h - self._margin * 2
        self._ox = self._margin + max(0.0, (aw - self._content_w) / 2)
        pad_y = max(0.0, (ah - self._content_h) / 2)
        self._oy = self._panel_h + self._margin + pad_y

    def _recompute_layout(self) -> None:
        self._map_h = self._win_h - self._panel_h
        self._scale = self._compute_scale()
        self._apply_scale()

    def _to_screen(self, x: int, y: int) -> tuple[int, int]:
        sx = int(self._ox + (x - self._min_x) * self._scale)
        sy = int(self._oy + self._content_h - (y - self._min_y) * self._scale)
        return sx, sy

    def _advance_tick(self) -> None:
        if self._tick < self._pf.total_ticks - 1:
            self._tick += 1
        else:
            self._playing = False

    # Main loop

    def run(self) -> None:
        running = True
        self._last_tick_ms = pygame.time.get_ticks()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self._win_w, self._win_h = event.w, event.h
                    self._screen = pygame.display.set_mode(
                        (self._win_w, self._win_h), pygame.RESIZABLE)
                    self._recompute_layout()
                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    if self._info_btn.collidepoint(event.pos):
                        self._show_info = not self._show_info
                    elif self._legend_btn.collidepoint(event.pos):
                        self._show_legend = not self._show_legend
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
            if self._show_info:
                self._draw_map_info()
            if self._show_legend:
                self._draw_legend()
            if self._show_solution:
                self._draw_solution_overlay()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > self._panel_h:
                hovered = self._hub_at(mouse_pos)
                if hovered:
                    self._draw_hover_tooltip(hovered, mouse_pos)
            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()

    # Drawing helpers

    def _blit_centered(self, surf: pygame.Surface, cx: int, cy: int) -> None:
        rect = surf.get_rect(center=(cx, cy))
        self._screen.blit(surf, rect)

    def _draw_bg_box(
        self, x: int, y: int, w: int, h: int,
        fill: tuple[int, ...], border: tuple[int, ...] | None = None,
        border_w: int = 1
    ) -> None:
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill(fill)
        if border is not None:
            pygame.draw.rect(bg, border, bg.get_rect(), border_w)
        self._screen.blit(bg, (x, y))

    def _draw_box(
        self, bx: int, by: int, box_w: int, box_h: int,
        surfs: list[pygame.Surface],
        fill: tuple[int, ...] = (10, 10, 28, 210),
        border: tuple[int, ...] = (90, 90, 140, 200),
    ) -> None:
        pad, line_gap = 10, 4
        line_h = surfs[0].get_height() + line_gap
        self._draw_bg_box(bx, by, box_w, box_h, fill, border)
        for i, surf in enumerate(surfs):
            self._screen.blit(surf, (bx + pad, by + pad + i * line_h))

    def _draw_diamond(
        self, color: tuple[int, int, int], center: tuple[int, int], r: int,
        border: tuple[int, int, int] = (255, 255, 255), border_w: int = 1
    ) -> None:
        cx, cy = center
        points = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
        pygame.draw.polygon(self._screen, color, points)
        if border_w:
            pygame.draw.polygon(self._screen, border, points, border_w)

    # Map drawing

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
            label = self._font_sm.render(str(cap), True, (200, 200, 220))
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
            color = self._resolve_color(hub.metadata.get('color', ''))
            pygame.draw.circle(self._screen, color, (sx, sy), r)
            pygame.draw.circle(
                self._screen, (255, 255, 255), (sx, sy), r, border)
            if not self._show_labels:
                continue

            if r >= 14:
                is_endpoint = hub.hub_type in ('start', 'end')
                cap = hub.metadata.get(
                    'max_drones', '' if is_endpoint else '1')
                if cap:
                    cap_surf = self._font_hub_inner.render(
                        str(cap), True, (0, 0, 0))
                    self._blit_centered(cap_surf, sx, sy)

                badge = self._badge_letter(hub)
                if badge:
                    badge_surf = self._font_hub_inner.render(
                        badge, True, (255, 255, 255))
                    bw, bh = badge_surf.get_size()
                    bx = sx - int(r * 0.6) - bw // 2
                    by = sy - int(r * 0.6) - bh // 2
                    self._draw_bg_box(
                        bx - 2, by - 1, bw + 4, bh + 2, (10, 10, 25, 220))
                    self._screen.blit(badge_surf, (bx, by))

    # Drones

    def _hub_at(self, pos: tuple[int, int]) -> Hub | None:
        mx, my = pos
        for hub in self.nav_map.hub_list:
            sx, sy = self._to_screen(hub.x, hub.y)
            if hypot(mx - sx, my - sy) <= max(self._hub_radius, 6):
                return hub
        return None

    def _draw_hover_tooltip(self, hub: Hub, pos: tuple[int, int]) -> None:
        is_endpoint = hub.hub_type in ('start', 'end')
        cap = hub.metadata.get(
            'max_drones', 'unlimited' if is_endpoint else '1')
        lines = [hub.name, f"Coords: ({hub.x}, {hub.y})"]
        if hub.hub_type:
            lines.append(f"Type: {hub.hub_type}")
        lines.append(f"Zone: {hub.zone or 'normal'}")
        lines.append(f"Color: {hub.metadata.get('color', 'none')}")
        lines.append(f"Capacity: {cap}")

        surfs, box_w, box_h = self._measure_lines(lines, (230, 230, 245))
        mx, my = pos
        bx = min(mx + 16, self._win_w - box_w - 4)
        by = min(my + 16, self._win_h - box_h - 4)
        self._draw_box(
            bx, by, box_w, box_h, surfs,
            (10, 10, 28, 235), (150, 150, 200, 230))

    def _draw_drones(self) -> None:
        if not self._pf.ticks:
            return
        cur = self._pf.ticks[self._tick]
        has_next = self._tick + 1 < len(self._pf.ticks)
        nxt = self._pf.ticks[self._tick + 1] if has_next else None
        prog = self._anim_progress if has_next else 0.0
        hub_by_name = {h.name: h for h in self.nav_map.hub_list}

        def _pos(entry: str | tuple[str, str]) -> tuple[int, int] | None:
            if isinstance(entry, tuple):
                ha, hb = hub_by_name.get(entry[0]), hub_by_name.get(entry[1])
                if not (ha and hb):
                    return None
                ax, ay = self._to_screen(ha.x, ha.y)
                bx, by = self._to_screen(hb.x, hb.y)
                return (ax + bx) // 2, (ay + by) // 2
            hub = hub_by_name.get(entry)
            return self._to_screen(hub.x, hub.y) if hub else None

        def _badge(pos: tuple[int, int], n: int) -> None:
            bx = pos[0] + int(self._hub_radius * 0.72)
            by = pos[1] - int(self._hub_radius * 0.72)
            r = self._drone_badge_r
            self._draw_diamond(RC.DRONE_COLOR, (bx, by), r)
            surf = self._font_hub_inner.render(str(n), True, (255, 255, 255))
            self._blit_centered(surf, bx, by)

        if prog > 0.0 and nxt is not None:
            at_rest: dict[str | tuple[str, str], int] = {}
            for c, n in zip(cur, nxt):
                if c == n:
                    at_rest[c] = at_rest.get(c, 0) + 1
                    continue
                pa, pb = _pos(c), _pos(n)
                if pa and pb:
                    dx = int(pa[0] + (pb[0] - pa[0]) * prog)
                    dy = int(pa[1] + (pb[1] - pa[1]) * prog)
                    r = max(11, self._drone_badge_r - 1)
                    self._draw_diamond(RC.DRONE_COLOR, (dx, dy), r)
            for entry, cnt in at_rest.items():
                pos = _pos(entry)
                if pos:
                    _badge(pos, cnt)
        else:
            count: dict[str | tuple[str, str], int] = {}
            for entry in cur:
                count[entry] = count.get(entry, 0) + 1
            for entry, cnt in count.items():
                pos = _pos(entry)
                if pos:
                    _badge(pos, cnt)

    # HUD overlays

    def _draw_map_info(self) -> None:
        bx = min(self._info_btn.x, self._win_w - self._info_box_w - 4)
        self._draw_box(
            bx, self._panel_h + 4, self._info_box_w, self._info_box_h,
            self._info_surfs)

    def _draw_legend(self) -> None:
        bx = min(self._legend_btn.x, self._win_w - self._legend_box_w - 4)
        self._draw_box(
            bx, self._panel_h + 4, self._legend_box_w, self._legend_box_h,
            self._legend_surfs)

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

        y = by + pad + title.get_height() + line_gap
        line_h = self._font_sm.get_height() + line_gap
        max_lines = max(1, (by + box_h - pad - y) // line_h)
        for i, line in enumerate(lines[:max_lines]):
            surf = self._font_sm.render(
                f"T{i + 1}: {line}", True, RC.SOLUTION_TEXT)
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

    def _draw_toggle_btn(
        self, label: str, x: int, active: bool
    ) -> pygame.Rect:
        surf = self._font_sm.render(label, True, (230, 230, 245))
        rect = pygame.Rect(x, 10, surf.get_width() + 16, self._panel_h - 20)
        fill = (70, 70, 120, 230) if active else (30, 30, 50, 200)
        self._draw_bg_box(rect.x, rect.y, rect.w, rect.h, fill,
                          (120, 120, 170, 220))
        self._blit_centered(surf, rect.centerx, rect.centery)
        return rect

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
        total = self._pf.total_ticks - 1
        flow = self._pf.flow_reached
        tick_txt = (f"{state}  |  Turn {self._tick} / {total}"
                    f"  |  Flow {flow} / {self.nav_map.nb_drones}")
        tick_col = (100, 220, 140) if self._playing else (220, 180, 80)
        tick_surf = self._font_sm.render(tick_txt, True, tick_col)
        ty = self._panel_h * 3 // 4 - tick_surf.get_height() // 2
        self._screen.blit(tick_surf, (14, ty))
        self._blit_centered(
            self._opts_surf, self._win_w // 2, self._panel_h * 3 // 4)
        self._legend_btn = self._draw_toggle_btn(
            "Legend", self._win_w - 90, self._show_legend)
        self._info_btn = self._draw_toggle_btn(
            "Info", self._legend_btn.x - 80, self._show_info)
