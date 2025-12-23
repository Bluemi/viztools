import pygame as pg
import numpy as np

from viztools.drawable import Points
from viztools.ui.elements import Button
from viztools.viewer import Viewer


class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__()

        self.points = Points(np.random.normal(size=(1000, 2)), size=0.05)
        self.button = Button(pg.Rect(50, 50, 120, 40), "Click me")

    def update(self):
        if self.button.is_clicked:
            print('clicked')


viewer = SimpleViewer()
viewer.run()
