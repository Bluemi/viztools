from abc import ABC, abstractmethod
from typing import Tuple, Dict, Iterable

import pygame as pg
import numpy as np

from viztools.coordinate_system import CoordinateSystem


ColorTuple = Tuple[int, int, int, int]


class Drawable(ABC):
    @abstractmethod
    def draw(self, screen: pg.Surface, coordinate_system: CoordinateSystem, screen_size: np.ndarray):
        pass


def _color_to_tuple(color: pg.Color | np.ndarray) -> ColorTuple:
    return color[0], color[1], color[2], color[3]


class Points(Drawable):
    def __init__(
            self, points: np.ndarray, size: int | float | Iterable[int | float] = 3,
            color: pg.Color | Iterable[pg.Color] | np.array = pg.Color(77, 178, 11)
    ):
        """
        Drawable to display a set of points.
        :param points: A list of points with the shape [N, 2] where N is the number of points.
        :param size: The radius of the points. If set to an integer, this is the radius on the screen in pixels. If set
                     to a float, this is the radius on the screen in units of the coordinate system. If set to a list,
                     it contains the sizes for each point.
        :param color: The color of the points.
        """
        # points
        if not isinstance(points, np.ndarray):
            raise TypeError(f'points must be a numpy array, not {type(points)}.')
        if points.ndim != 2 or points.shape[1] != 2:
            raise ValueError(f'points must be numpy array with shape (N, 2), not {points.shape}.')
        n_points = len(points)
        self._points = points

        # size
        if isinstance(size, (int, float)):
            is_relative_size = isinstance(size, float)
            size = np.repeat(np.array([[size, float(is_relative_size)]], dtype=np.float32), n_points, axis=0)
        elif isinstance(size, np.ndarray):
            if size.shape != (n_points,):
                raise ValueError(f'size must be a numpy array with shape ({n_points},), not {size.shape}.')
            is_relative_size = np.full(n_points, np.issubdtype(size.dtype, np.floating), dtype=np.float32)
            size = np.stack([size.astype(np.float32), is_relative_size], axis=1)
        elif isinstance(size, list):
            if len(size) != n_points:
                raise ValueError(f'size must be a list of length {n_points}, not {len(size)}.')
            size = [[s, isinstance(s, float)] for s in size]
            size = np.array(size, dtype=np.float32)
        else:
            raise TypeError(f'size must be an integer, float or iterable, not {type(size)}.')
        self._size = size

        # colors
        if isinstance(color, pg.Color):
            color = np.array([_color_to_tuple(color)] * n_points, dtype=np.float32)
        elif not isinstance(color, np.ndarray):
            color = np.array([_color_to_tuple(c) for c in color], dtype=np.float32)
        if color.shape != (n_points, 4):
            raise ValueError(f'colors must be a numpy array with shape ({n_points}, 4), not {color.shape}.')
        self._colors = color

        self._surface_parameters = {}
        for surf_params in self._get_surf_params():
            self._surface_parameters[surf_params.tobytes()] = surf_params

    def __len__(self):
        return len(self._points)

    def _get_surf_params(self) -> np.ndarray:
        return np.concatenate([self._size, self._colors], axis=1)

    def _get_surf_param(self, index: int) -> np.ndarray:
        return np.concatenate([self._size[index, :], self._colors[index, :]], axis=0)

    def set_color(self, color: pg.Color | Tuple[int, int, int], index: int):
        color = _color_to_tuple(color)
        self._colors[index, :] = color
        self._update_surf_params(index)

    def _update_surf_params(self, index: int):
        surf_params = self._get_surf_param(index)
        self._surface_parameters[surf_params.tobytes()] = surf_params

    def set_size(self, size: int | float, index: int):
        self._size[index, 0] = size
        self._size[index, 1] = isinstance(size, float)
        self._update_surf_params(index)

    def _create_point_surfaces(self, zoom_factor: float) -> Dict[bytes, pg.Surface]:
        surfaces = {}
        for k, surf_params in self._surface_parameters.items():
            draw_size = _get_draw_size(surf_params[0], zoom_factor, bool(surf_params[1]))
            color = surf_params[2:]

            # old version with per pixel alpha
            # point_surface = pg.Surface((draw_size * 2, draw_size * 2), pg.SRCALPHA)
            # point_surface.fill((0, 0, 0, 0))
            point_surface = pg.Surface((draw_size * 2, draw_size * 2))
            point_surface.set_colorkey((0, 0, 0), pg.RLEACCEL)
            point_surface.set_alpha(int(color[3]), pg.RLEACCEL)
            pg.draw.circle(point_surface, color, (draw_size, draw_size), draw_size)

            surfaces[k] = point_surface
        return surfaces

    def _get_draw_sizes(self, zoom_factor: float) -> np.ndarray:
        """
        Computes the draw sizes for the given sizes and coordinate system.
        :param zoom_factor: A float defining the scale factor for relative sizes.
        size[i] must be multiplied with zoom_factor.
        :return: numpy array of integers of shape [N,] where N is the number of sizes.
        """
        draw_sizes = self._size[:, 0].copy()
        is_relative_size = self._size[:, 1] > 0.5
        draw_sizes[is_relative_size] *= zoom_factor
        return np.maximum(draw_sizes.astype(int), 1)

    def draw(self, screen: pg.Surface, coordinate_system: CoordinateSystem, screen_size: np.ndarray):
        draw_sizes = self._get_draw_sizes(coordinate_system.zoom_factor)

        # filter out invalid positions
        screen_points = coordinate_system.space_to_screen(self._points.T).T
        valid_positions = _get_valid_positions(screen_points, draw_sizes, screen_size)
        screen_points = screen_points[valid_positions]
        valid_colors = self._colors[valid_positions]
        valid_sizes = draw_sizes[valid_positions]
        screen_points -= valid_sizes.reshape(-1, 1)

        # create blit surfaces
        surfaces = self._create_point_surfaces(coordinate_system.zoom_factor)

        # draw
        for pos, size, color, surf_params in zip(
                screen_points, valid_sizes, valid_colors, self._get_surf_params()[valid_positions]
        ):
            surface = surfaces[surf_params.tobytes()]
            screen.blit(surface, pos)

    def clicked_points(self, event: pg.event.Event, coordinate_system: CoordinateSystem) -> np.ndarray:
        """
        Returns the indices of the points clicked by the mouse. Returns an empty array if no point was clicked.

        :param event: The event to check.
        :param coordinate_system: The coordinate system to use.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            draw_size = self._get_draw_sizes(coordinate_system.zoom_factor)

            screen_pos = np.array(event.pos).reshape(1, 2)
            screen_points = coordinate_system.space_to_screen(self._points.T).T
            distances = np.linalg.norm(screen_points - screen_pos, axis=1)
            return np.nonzero(distances < draw_size)[0]
        return np.array([])


def _get_draw_size(
        size: float, zoom_factor: float, is_relative_size: bool
) -> int:
    if is_relative_size:
        size = max(int(size * zoom_factor), 1)
    return int(size)


def _get_valid_positions(screen_points: np.ndarray, draw_sizes: np.ndarray, screen_size: np.ndarray) -> np.ndarray:
    return np.where(np.logical_and(
        np.logical_and(screen_points[:, 0] > -draw_sizes, (screen_points[:, 0] < screen_size[0] + draw_sizes)),
        np.logical_and(screen_points[:, 1] > -draw_sizes, (screen_points[:, 1] < screen_size[1] + draw_sizes))
    ))[0]


def to_draw_positions(
        points: np.ndarray, coordinate_system: CoordinateSystem, valid_positions: np.ndarray
) -> np.ndarray:
    """
    Converts a list of points to a list of positions to draw them on the screen.
    Filters out points outside the screen.

    :param points: Numpy array of shape [N, 2] where N is the number of points.
    :param coordinate_system: The coordinate system to use.
    :param valid_positions: Array with shape [N], where N is the number of points. This array contains booleans
                            indicating whether the point is visible on the screen.
    :return: Numpy array with shape [K, 2] where K is the number of valid points that are visible on the screen.
    """
    screen_points = coordinate_system.space_to_screen(points.T).T
    return screen_points[valid_positions].astype(int)
