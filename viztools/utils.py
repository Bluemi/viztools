import enum
import warnings
from typing import Union, Tuple

import pygame as pg
import numpy as np

DEFAULT_FONT_SIZE = 16


def to_np_array(p):
    if isinstance(p, np.ndarray):
        return p
    return np.array(p)


ColorType = Union[Tuple[int, int, int], pg.Color]


class RenderContext:
    def __init__(self, font: pg.font.Font):
        self.font = font
        self.mouse_pressed = False

    @staticmethod
    def default(font_size: int = DEFAULT_FONT_SIZE):
        font = load_font(font_size)
        return RenderContext(font)


class Align(enum.StrEnum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"

    def align_in(self, rect: pg.Rect, container: pg.Rect) -> pg.Rect:
        new_rect = rect.copy()
        if self == Align.CENTER:
            new_rect.center = container.center
        elif self == Align.LEFT:
            new_rect.midleft = container.midleft
        elif self == Align.RIGHT:
            new_rect.midright = container.midright
        elif self == Align.TOP:
            new_rect.midtop = container.midtop
        elif self == Align.BOTTOM:
            new_rect.midbottom = container.midbottom
        else:
            raise ValueError(f"Invalid alignment: {self}")
        return new_rect


def load_font(font_size: int = DEFAULT_FONT_SIZE):
    """
    Helper function to load the default font.
    :return: The font to use
    """
    try:
        font = pg.font.Font(None, font_size)
    except pg.error:
        warnings.warn("Warning: Could not load default font. Text will not be rendered.")
        font = None
    return font


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
