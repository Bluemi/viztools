#!/usr/bin/env python3
from pathlib import Path

from PIL import Image as PilImage

import pygame as pg
import numpy as np

from viztools.drawable import Points, Image, Lines, OverlayText
from viztools.ui.container.base_container import UIContainer
from viztools.ui.elements import Button, Label, EditField, TextField
from viztools.utils import Align
from viztools.viewer import Viewer


class Menu(UIContainer):
    def __init__(self):
        super().__init__(False)
        self.label = Label(pg.Rect(50, 100, 120, 40), "This is text :)", align=Align.LEFT)
        self.edit_field = EditField(pg.Rect(200, 50, 220, 40), "Edit me...")
        self.text_field = TextField(
            pg.Rect(200, 100, 520, 440),
            "This is a long text :).\nIt supports multi-lines, copy-paste, selection, ..."
        )
        self.btn_show_image = Button(pg.Rect(50, 150, 120, 40), "Show Image")


def create_line_points() -> np.ndarray:
    """Create a spiral pattern with varying radius"""
    n = 200
    t = np.linspace(0, 4 * np.pi, n)
    radius = np.linspace(0.01, 3, n)
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    return np.column_stack([x, y])


class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__()

        self.lines = Lines(
            create_line_points(),
            color=np.array([0, 80, 80]),
        )

        self.points = Points(
            np.random.normal(size=(1000, 2)) * 2,
            size=0.05,
            color=np.array([0, 255, 0, 50]),
            chunk_size=400.0
        )

        path = Path('images/noodles_deliveryman.png')
        if path.is_file():
            with PilImage.open(path) as image:
                self.image = Image(image, np.array([6, 0]), size=0.005, align=Align.TOP, visible=False)
        else:
            self.image = OverlayText(f'Image file not found: {path}', np.array([6, -0.5]), font_size=32, visible=False)
        self.image_caption = OverlayText('Noodle Deliveryman', np.array([6, 0.2]), font_size=0.2, visible=False)

        self.button = Button(pg.Rect(50, 50, 120, 40), "Open Menu")

        self.menu = Menu()

    def update(self):
        if self.button.is_clicked:
            self.menu.visible = not self.menu.visible
        if self.menu.btn_show_image.is_clicked:
            if self.image is not None:
                self.image.visible = not self.image.visible
                self.image_caption.visible = self.image.visible


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
