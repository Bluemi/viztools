#!/usr/bin/env python3
import numpy as np
import pygame as pg

from viztools.drawable import Points
from viztools.viewer import Viewer

class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__()
        self.points = Points(
            np.array([[0, 0], [1, 1], [-1, 2]]), size=0.2
        )

    def tick(self, delta_time: float):
        pass

    def render(self):
        self.render_coordinate_system()
        self.render_drawables([self.points])

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)
        for p_index in self.points.clicked_points(event, self.coordinate_system):
            self.points.colors[p_index] = pg.Color(255, 0, 0)


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
