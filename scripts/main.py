#!/usr/bin/env python3

import pygame as pg
import numpy as np

from viztools.drawable.overlay_text import OverlayText
from viztools.drawable.points import Points
from viztools.viewer import Viewer


class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__(drag_mouse_button=3)
        num_points = 1_000_000
        positions = np.random.random(size=(num_points, 2))
        positions[:, 0] *= 20
        positions[:, 1] *= 40
        self.points = Points(
            positions,
            # np.array([[0, 0], [1, 1], [-1, 2]]),
            # size=np.random.randint(1, 5, size=num_points) ** 2 / 250,
            size=10,
            color=np.array([0, 255, 0, 50])
        )
        # self.points = Points(
        #     np.array([[0, 0], [1, 0], [2, 0]]),
        #     size=0.5,
        #     color=np.array([0, 255, 255, 50])
        # )
        # point types:
        # 0 - normal
        # 1 - hovered
        # 2 - clicked
        self.point_type: np.ndarray = np.zeros(len(self.points), dtype=np.int8)
        self.overlay_text = OverlayText(
            # 'This is short\n' + 'This is some longer text\n' * 20,
            'Label',
            np.array([0.5, 0.5]),
            font_size=0.1,
            color=np.array([128, 128, 128]),
            # background_color=np.array([50, 50, 50, 128]),
            border_color=np.array([80, 80, 80, 128]),
        )

    def tick(self, delta_time: float):
        self.update_drawables([self.points])

    def render(self):
        self.render_coordinate_system(draw_numbers=True)
        self.render_drawables([self.points, self.overlay_text])

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)
        # if event.type == pg.MOUSEMOTION:
        #     clicked_indices = np.nonzero(np.equal(self.point_type, 2))[0]
        #     old_hovered = np.nonzero(np.equal(self.point_type, 1))[0]
        #     hovered_indices = self.points.hovered_points(self.mouse_pos, self.coordinate_system)
        #     hovered_indices = np.setdiff1d(hovered_indices, clicked_indices)
        #     if not np.array_equal(old_hovered, hovered_indices):
        #         self.point_type[old_hovered] = 0
        #         self.point_type[hovered_indices] = np.maximum(1, self.point_type[hovered_indices])
        #         for oh in old_hovered:
        #             self.points.set_color(np.array([0, 255, 0, 50]), oh)
        #         for hi in hovered_indices:
        #             self.points.set_color(np.array([0, 255, 0, 100]), hi)
        #         self.render_needed = True

        # if event.type == pg.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         old_clicked = np.nonzero(np.equal(self.point_type, 2))[0]
        #         self.point_type[old_clicked] = 0
        #         for p_index in old_clicked:
        #             self.points.set_color(np.array([0, 255, 0, 50]), p_index)

        #         # clicked_indices = self.points.clicked_points(event, self.coordinate_system)
        #         # if len(clicked_indices) > 0:
        #         #     self.point_type[clicked_indices] = 2
        #         #     for p_index in clicked_indices:
        #         #         self.points.set_color(np.array([255, 0, 0, 50]), p_index)

        #         closest_point, dist = self.points.closest_point(self.mouse_pos, self.coordinate_system)
        #         if dist < 10:
        #             self.point_type[closest_point] = 2
        #             self.points.set_color(np.array([255, 0, 0, 50]), closest_point)
        #         self.render_needed = True


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
