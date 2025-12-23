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


Color = Union[np.ndarray, Tuple[int, int, int, int], Tuple[int, int, int]]


def normalize_color(color: Color) -> np.ndarray:
    if len(color) == 3:
        return np.array([*color, 255], dtype=np.float32)
    if len(color) != 4:
        raise ValueError(f'color must be of length 3 or 4, not {len(color)}.')
    return np.array(color, dtype=np.float32)


class RenderContext:
    def __init__(self, font: pg.font.Font):
        self.font = font
        self.mouse_pressed = False

    @staticmethod
    def default(font_size: int = DEFAULT_FONT_SIZE):
        font = load_font(font_size)
        return RenderContext(font)


class Align(enum.StrEnum):
    CENTER = 'center'
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'
    TOP_LEFT = 'top_left'
    TOP_RIGHT = 'top_right'
    BOTTOM_LEFT = 'bottom_left'
    BOTTOM_RIGHT = 'bottom_right'

    def arrange_rect(self, rect: pg.Rect, position: Union[np.ndarray, Tuple[int, int]]) -> pg.Rect:
        new_rect = rect.copy()

        if self == Align.CENTER:
            new_rect.center = position
        elif self == Align.LEFT:
            new_rect.midleft = position
        elif self == Align.RIGHT:
            new_rect.midright = position
        elif self == Align.TOP:
            new_rect.midtop = position
        elif self == Align.BOTTOM:
            new_rect.midbottom = position
        elif self == Align.TOP_LEFT:
            new_rect.topleft = position
        elif self == Align.TOP_RIGHT:
            new_rect.topright = position
        elif self == Align.BOTTOM_LEFT:
            new_rect.bottomleft = position
        elif self == Align.BOTTOM_RIGHT:
            new_rect.bottomright = position
        else:
            raise ValueError(f'unknown anker type: {self}')

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
