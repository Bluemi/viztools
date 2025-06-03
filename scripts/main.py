#!/usr/bin/env python3
import pygame as pg

from pygame_viztools.viewer import Viewer

class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__()

    def tick(self, delta_time: float):
        pass

    def render(self):
        pass

    def handle_event(self, event: pg.event.Event):
        super().handle_event(event)


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
