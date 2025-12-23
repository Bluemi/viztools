from abc import ABC, abstractmethod
from typing import List

import pygame as pg

from viztools.coordinate_system import CoordinateSystem
from viztools.utils import RenderContext


class Drawable(ABC):
    def __init__(self):
        self.render_needed = False

    def handle_events(
            self, events: List[pg.event.Event], screen: pg.Surface, coordinate_system: CoordinateSystem,
            render_context: RenderContext
    ) -> List[pg.event.Event]:
        """
        Handles the given events and updates the element, if needed.
        If a redraw is necessary, sets self.render_needed to True.

        :param events: The events to handle.
        :param screen: The screen that will be used for drawing.
        :param coordinate_system: The coordinate system, this drawable is rendered in.
        :return: A list of events, that were not handled by this drawable.
        """
        unhandled_events = []
        for event in events:
            if not self.handle_event(event, screen, coordinate_system, render_context):
                unhandled_events.append(event)
        self.update(screen, coordinate_system, render_context)

        return unhandled_events

    @abstractmethod
    def handle_event(
            self, event: pg.event.Event, screen: pg.Surface, coordinate_system: CoordinateSystem,
            render_context: RenderContext
    ) -> bool:
        """
        Handles the given events and updates the element.
        :param event: The event to handle.
        :param screen: The screen that will be used for drawing.
        :param coordinate_system: The coordinate system, this drawable is rendered in.
        :param render_context: The render context used for drawing.
        :return: Whether the event was handled.
        """
        pass

    @abstractmethod
    def update(self, screen: pg.Surface, coordinate_system: CoordinateSystem, render_context: RenderContext):
        """
        Updates the element. Also sets self.render_needed to True, if needed.

        :param screen: The screen that will be used for drawing.
        :param coordinate_system: The coordinate system, this drawable is rendered in.
        """
        pass

    def draw(self, screen: pg.Surface, coordinate_system: CoordinateSystem, render_context: RenderContext):
        """
        Draws the element to the screen.

        :param screen: The screen that will be used for drawing.
        :param coordinate_system: The coordinate system, this drawable is rendered in.
        :param render_context: The render context used for drawing.
        """
        self.render(screen, coordinate_system, render_context)
        self.finalize()

    @abstractmethod
    def render(self, screen: pg.Surface, coordinate_system: CoordinateSystem, render_context: RenderContext):
        """
        Draws the element to the screen.

        :param screen: The screen that will be used for drawing.
        :param coordinate_system: The coordinate system, this drawable is rendered in.
        :param render_context: The render context used for drawing.
        """
        pass

    def finalize(self):
        """
        Finalize this drawable.
        """
        pass
