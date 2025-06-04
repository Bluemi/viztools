#!/usr/bin/env python3
import numpy as np
import pygame as pg

from viztools.drawable import Points
from viztools.viewer import Viewer

class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__()
        self.points = Points(
            np.random.normal(size=(200000, 2)) * 5,
            # np.array([[0, 0], [1, 1], [-1, 2]]),
            size=10,
            colors=pg.Color(0, 255, 0, 50)
        )

    def render(self):
        self.render_coordinate_system()
        self.render_drawables([self.points])

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)
        for p_index in self.points.clicked_points(event, self.coordinate_system):
            self.points.set_color(pg.Color(255, 0, 0), p_index)


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
