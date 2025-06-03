from abc import ABC, abstractmethod
from typing import List, Tuple

import pygame as pg
import numpy as np

from pygame_viztools.coordinate_system import CoordinateSystem


class Drawable(ABC):
    @abstractmethod
    def draw(self, screen: pg.Surface, coordinate_system: CoordinateSystem):
        pass


class Points(Drawable):
    def __init__(self, points: np.ndarray, size: int | float = 3, color: pg.Color = pg.Color(77, 178, 11)):
        """
        Drawable to display a set of points.
        :param points: A list of points with the shape [N, 2] where N is the number of points.
        :param size: The radius of the points. If set to an integer, this is the radius on the screen in pixels. If set
                     to a float, this is the radius on the screen in units of the coordinate system.
        """
        self.points = points
        self.size = size
        self.color = color

    def draw(self, screen: pg.Surface, coordinate_system: CoordinateSystem):
        screen_points = to_draw_positions(self.points, coordinate_system)
        draw_size = self.size
        if isinstance(draw_size, float):
            draw_size = max(int(draw_size * coordinate_system.zoom_factor), 1)
        for pos in screen_points:
            pg.draw.circle(screen, self.color, pos, draw_size)


def to_draw_positions(points: np.ndarray, coordinate_system: CoordinateSystem) -> List[Tuple[int, int]]:
    screen_points = coordinate_system.space_to_screen(points.T)
    return screen_points_to_tuple_list(screen_points)


def screen_points_to_tuple_list(screen_points: np.ndarray) -> List[Tuple[int, int]]:
    # noinspection PyTypeChecker
    return [tuple(p) for p in screen_points.astype(int).T.tolist()]
