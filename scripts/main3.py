#!/usr/bin/env python3

import pygame as pg
import numpy as np

from viztools.drawable.lines import Lines
from viztools.viewer import Viewer


class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__(drag_mouse_button=3)
        num_lines = 10
        positions = np.random.random(size=(num_lines, 2))
        positions *= 10
        self.lines = Lines(
            positions,
            color=np.array([0, 255, 0, 50]),
        )

    def tick(self, delta_time: float):
        self.update_drawables([self.lines])

    def render(self):
        self.render_coordinate_system(draw_numbers=True)
        self.render_drawables([self.lines])

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
