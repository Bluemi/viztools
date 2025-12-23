from typing import Tuple, Optional, List, Union, Iterable

import pygame as pg

from .elements.base_element import UIElement
from .container import Container


class Viewer:
    def __init__(self, title: str = "Window", screen_size: Tuple[int, int] = (800, 600), flags: int = 0):
        self._element_cache: Optional[List[Union[Container, UIElement]]] = None

    def run(self):
        while self.running:
            self.handle_events()
            self.tick()
            self.render()

        pg.quit()

    def iter_elements(self) -> Iterable[Union[UIElement, Container]]:
        """
        Iter over all elements in the container.
        :return: Iterable of BaseElement objects.
        """
        if self._element_cache is None:
            self._element_cache = [elem for elem in self.__dict__.values() if isinstance(elem, (UIElement, Container))]

        yield from self._element_cache

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            for elem in self.iter_elements():
                elem.handle_event(event)

    def tick(self):
        pass

    def render(self):
        self.screen.fill(0)
        for elem in self.iter_elements():
            elem.render(self.screen, self.render_context)
        pg.display.flip()
