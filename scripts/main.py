#!/usr/bin/env python3
import numpy as np
import pygame as pg

from viztools.drawable import Points
from viztools.render_backend.events import Event
from viztools.viewer import Viewer

class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__()
        self.points = Points(
            np.random.normal(size=(200000, 2)) * 5,
            # np.array([[0, 0], [1, 1], [-1, 2]]),
            size=np.random.randint(1, 5, size=200000) ** 2 / 250,
            # size=5,
            color=np.array([0, 255, 0, 50])
        )
        self.marked_indices = np.zeros(len(self.points), dtype=bool)

    def render(self):
        self.render_coordinate_system()
        self.render_drawables([self.points])

    def handle_event(self, event: Event):
        super().handle_event(event)
        clicked_indices = self.points.clicked_points(event, self.coordinate_system)
        if len(clicked_indices) > 0:
            self.marked_indices[clicked_indices] = 1 - self.marked_indices[clicked_indices]
            for p_index in clicked_indices:
                color = np.array([255, 0, 0]) if self.marked_indices[p_index] else np.array([0, 255, 0, 50])
                self.points.set_color(color, p_index)


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
