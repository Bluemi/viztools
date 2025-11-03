#!/usr/bin/env python3

from PIL import Image as PilImage

import pygame as pg
import numpy as np

from viztools.drawable.draw_utils import AnkerType
from viztools.drawable.image import Image
from viztools.drawable.lines import Lines
from viztools.viewer import Viewer


class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__(drag_mouse_button=2)
        with PilImage.open('images/n02085936_7515.jpg') as image:
            self.image = Image(image, np.array([0, 0]), anker_type=AnkerType.TOP)
        num_lines = 10
        positions = np.random.random(size=(num_lines, 2))
        positions *= 10
        self.lines = Lines(
            positions,
            color=np.array([0, 255, 0, 50]),
        )

    def tick(self, delta_time: float):
        self.update_drawables([self.lines, self.image])

    def render(self):
        self.render_coordinate_system(draw_numbers=True)
        self.render_drawables([self.lines, self.image])

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)
        clicked_points = self.lines.clicked_points(event, self.coordinate_system)
        if clicked_points.shape[0] > 0:
            print(clicked_points)


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
