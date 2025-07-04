from typing import Self, Tuple, Optional

import numpy as np


class ChunkGrid:
    def __init__(
            self, surfaces: np.ndarray, point_chunk_indices: np.ndarray, chunk_point_indices: np.ndarray,
            left_bot: np.ndarray, chunk_size: float
    ):
        """
        Creates a new ChunkGrid object. This groups the given points into a grid of chunks with size (w, h).
        Each chunk consists of a pg.Surface, a rect in world coordinates defining which points are in the chunk and
        points-indices of the points in the chunk.

        :param surfaces: A numpy array with shape (w, h) of type pg.Surface.
        :param point_chunk_indices: A numpy array with shape n of type int. Accessing point_indices[i] gives the
        chunk_index of the ith point. Left bottom chunk has index 0, the next chunk to the top has index 1.
        The top right chunk as index h*w-1.
        :param chunk_point_indices: A numpy array with shape (w, h) of type int. Accessing point_indices[x, y] gives
        a numpy array of indices for points in the chunk at (x, y).
        :param left_bot: The world coordinates of the bottom left corner of the bottom left chunk as a numpy array with
        shape 2 of type float.
        :param chunk_size: The size of the chunks in world coordinates.
        """
        self.surfaces = surfaces
        self.point_chunk_indices = point_chunk_indices
        self.chunk_point_indices = chunk_point_indices
        self.left_bot = left_bot
        self.chunk_size = chunk_size
        # meaning of status:
        # - 0: not rendered
        # - 1: has to update
        # - 2: ok
        self.status = np.zeros(surfaces.shape, dtype=np.int32)

    def shape(self) -> Tuple[int, int]:
        """
        The number of chunks in the grid as tuple (w, h).
        """
        return self.surfaces.shape

    @classmethod
    def from_points(cls, points: np.ndarray, chunk_size: float) -> Self:
        """
        Create a grid of chunks from the given points. Each point is in exactly one chunk.
        Chunks are created in scanline order.

        :param points: The center positions of points in the coordinate system with shape (n, 2).
        Accessing points[i] gives the (x, y) position of point i.
        :param chunk_size: The maximum size of a chunk in world size.
        :return: A ChunkGrid object.
        """
        if points.ndim != 2 or points.shape[1] != 2:
            raise ValueError(f'points must be a numpy array with shape (n, 2), not {points.shape}.')
        if not np.issubdtype(points.dtype, np.floating):
            raise ValueError(f'points must be a numpy array with floating point values, not {points.dtype}.')

        most_left_bot = np.min(points, axis=0)
        most_right_top = np.max(points, axis=0)

        world_size = most_right_top - most_left_bot
        chunks_shape = np.trunc(world_size / chunk_size).astype(np.int32) + 1

        surfaces = np.full(chunks_shape, None, dtype=object)  # numpy array of pg.Surface

        points_rel_to_bot_left = points - most_left_bot.reshape(1, 2)
        chunk_indices_per_axis = np.trunc(points_rel_to_bot_left / chunk_size)
        for dim in range(2):
            chunk_indices_per_axis[:, dim] = np.clip(chunk_indices_per_axis[:, dim], 0, chunks_shape[dim]-1)

        # index = x * h + y
        point_chunk_indices: np.ndarray = chunk_indices_per_axis[:, 1] + chunk_indices_per_axis[:, 0] * chunks_shape[1]

        chunks_point_indices = np.full(chunks_shape, None, dtype=object)
        for chunk_x in range(chunks_shape[0]):
            for chunk_y in range(chunks_shape[1]):
                current_chunk_index: int = chunk_x * chunks_shape[1] + chunk_y
                cur_chunk = np.nonzero(np.equal(point_chunk_indices, current_chunk_index))[0]
                chunks_point_indices[chunk_x, chunk_y] = cur_chunk

        return ChunkGrid(surfaces, point_chunk_indices, chunks_point_indices, most_left_bot, chunk_size)
    
    def get_in_viewport_chunk_indices(self, viewport: np.ndarray) -> np.ndarray:
        """
        Get chunk indices in the viewport.

        :param viewport: Numpy array of shape (2, 2) with the viewport coordinates in world coordinates.
        Accessing viewport[0] gives the top left corner of the viewport in world coordinates. Accessing viewport[1]
        gives the bottom right corner of the viewport in world coordinates.
        """
        # Convert viewport coordinates to chunk indices
        rel_viewport = (viewport - self.left_bot.reshape(1, 2)) / self.chunk_size
        left = np.trunc(rel_viewport[0, 0]).astype(np.int32)
        top = np.ceil(rel_viewport[0, 1]).astype(np.int32) - 1
        right = np.ceil(rel_viewport[1, 0]).astype(np.int32) - 1
        bot = np.trunc(rel_viewport[1, 1]).astype(np.int32)

        left_right = np.clip([left, right], 0, self.shape()[0]-1)
        bot_top = np.clip([bot, top], 0, self.shape()[1]-1)

        # Create grid of all chunk positions between top-left and bottom-right
        x = np.arange(left_right[0], left_right[1] + 1)
        y = np.arange(bot_top[0], bot_top[1] + 1)
        x_axis, y_axis = np.meshgrid(x, y)

        # Convert to linear indices (x * h + y)
        return x_axis.flatten() * self.shape()[1] + y_axis.flatten()

    def get_next_update_chunk(self, viewport: np.ndarray) -> Optional[int]:
        """
        Calculates the chunk index of the next chunk to draw.
        
        :param viewport: Numpy array of shape (2, 2) with the viewport coordinates in world coordinates.
        Accessing viewport[0] gives the top left corner of the viewport in world coordinates. Accessing viewport[1]
        gives the bottom right corner of the viewport in world coordinates.
        """
        chunk_indices = self.get_in_viewport_chunk_indices(viewport)
        chunk_status = self.status.flat[chunk_indices]
        most_needed_index = np.argmin(chunk_status)
        if chunk_status[most_needed_index] == 2:
            return None
        return int(chunk_indices[most_needed_index])

    def set_status(self, chunk_index: int, status: int):
        self.status.flat[chunk_index] = status
