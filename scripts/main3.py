#!/usr/bin/env python3

from PIL import Image as PilImage

import pygame as pg
import numpy as np

from viztools.drawable import Points, Image, Lines, OverlayText
from viztools.ui.container.base_container import Container
from viztools.ui.elements import Button, Label, EditField, TextField
from viztools.utils import Align
from viztools.viewer import Viewer


class UIContainer(Container):
    def __init__(self):
        super().__init__()
        self.label = Label(pg.Rect(50, 100, 120, 40), "This is text :)", align=Align.LEFT)
        self.edit_field = EditField(pg.Rect(200, 50, 220, 40), "Edit me...")
        self.text_field = TextField(
            pg.Rect(200, 100, 520, 440),
            "This is a long text :).\nIt supports multi-lines, copy-paste, selection, ..."
        )


class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__(drag_mouse_button=2)

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

        with PilImage.open('images/n02085936_7515.jpg') as image:
            self.image = Image(image, np.array([6, 0]), align=Align.TOP)

        self.button = Button(pg.Rect(50, 50, 120, 40), "Click Me!")

        self.ui = UIContainer()

    def update(self):
        if self.button.is_clicked:
            self.ui.visible = not self.ui.visible


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
