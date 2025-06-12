from typing import List, Tuple, Self

import numpy as np
import pygame as pg

from .base_render_backend import RenderBackend, Surface, Font
from .events import Event


class PygameFont(Font):
    def __init__(self, font: pg.font.Font, font_name: str, font_size: int):
        super().__init__(font_name, font_size)
        self.font = font

    def render(self, text: str, color: np.ndarray, antialias: bool, background: np.ndarray = None) -> Surface:
        return PygameSurface(self.font.render(text, antialias, color, background))


class PygameSurface(Surface):
    def __init__(self, surface: pg.Surface):
        super().__init__()
        self.surface = surface

    def get_size(self) -> Tuple[int, int]:
        return self.surface.get_size()

    def fill(self, color: np.ndarray):
        self.surface.fill(color)

    def line(self, color: np.ndarray, start: np.ndarray, end: np.ndarray):
        pg.draw.line(self.surface, color, start, end)

    def circle(self, color: np.ndarray, pos: Tuple[int, int] | np.ndarray, radius: int):
        pg.draw.circle(self.surface, color, pos, radius)

    def blit(self, surface: Self, pos: Tuple[int, int]):
        self.surface.blit(surface.surface, pos)


class PygameBackend(RenderBackend):
    def init(self):
        pg.init()

    def quit(self):
        pg.quit()

    def get_font(self, font_size: int, font_name: str = '') -> PygameFont:
        font_name = font_name or pg.font.get_default_font()
        return PygameFont(pg.font.Font(font_name, font_size), font_name, font_size)

    def set_key_repeat(self, delay: int, interval: int):
        pg.key.set_repeat(delay, interval)

    def create_window(self, title: str, size: Tuple[int, int] = (0, 0)) -> PygameSurface:
        mode = pg.FULLSCREEN if size == (0, 0) else pg.RESIZABLE
        return PygameSurface(pg.display.set_mode(size, mode))

    def create_surface(self, size: Tuple[int, int], enable_alpha: bool = True) -> Surface:
        flags = 0
        if enable_alpha:
            flags = flags | pg.SRCALPHA
        return PygameSurface(pg.Surface(size, flags))

    def swap_buffers(self):
        pg.display.flip()

    def get_events(self) -> List[Event]:
        pass

    def draw_circle(self, surface: Surface, color: np.ndarray, pos: np.ndarray, radius: np.ndarray | float):
        pass
