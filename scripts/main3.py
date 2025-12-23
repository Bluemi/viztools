#!/usr/bin/env python3

import argparse
from PIL import Image as PilImage

import pygame as pg
import numpy as np

from viztools.drawable import Points, Image, Lines, OverlayText
from viztools.ui.elements import Button, Label, EditField, TextField
from viztools.utils import Align
from viztools.viewer import Viewer


class SimpleViewer(Viewer):
    def __init__(self, n_images: int = 1):
        super().__init__(drag_mouse_button=2)
        self.images = []
        for i in range(n_images):
            with PilImage.open('images/n02085936_7515.jpg') as image:
                # image = np.array(image)
                self.images.append(Image(image, np.array([i*6, 0]), align=Align.TOP))
        num_lines = 10
        positions = np.random.random(size=(num_lines, 2))
        positions *= 10
        self.lines = Lines(
            positions,
            color=np.array([0, 255, 0, 50]),
        )

        self.points = Points(
            np.random.normal(size=(20, 2)) * 2,
            size=0.05,
            color=np.array([0, 255, 0, 50]),
            chunk_size=400.0
        )

        self.overlay_text = OverlayText(
            'hello world', np.array([0, 1])
        )

        self.button = Button(pg.Rect(50, 50, 120, 40), "Click Me!")
        self.label = Label(pg.Rect(50, 100, 120, 40), "This is text :)", align=Align.LEFT)
        self.edit_field = EditField(pg.Rect(200, 50, 220, 40), "Edit me...")
        self.text_field = TextField(
            pg.Rect(200, 100, 520, 440),
            "This is a long text :).\nIt supports multi-lines, copy-paste, selection, ..."
        )

    def render(self):
        self.render_coordinate_system(draw_numbers=True)
        self.render_drawables([self.lines, self.points, self.overlay_text])
        self.render_drawables(self.images)

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)
        clicked_points = self.lines.clicked_points(event, self.coordinate_system)
        if clicked_points.shape[0] > 0:
            print(clicked_points)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n_images', type=int, default=1, nargs='?')
    return parser.parse_args()


def main():
    args = get_args()
    viewer = SimpleViewer(args.n_images)
    viewer.run()


if __name__ == '__main__':
    main()
