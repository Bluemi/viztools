from abc import ABC, abstractmethod
from typing import final, List

import pygame as pg

from viztools.utils import RenderContext


class UIElement(ABC):
    """
    Defines a base element class with different methods to implement functionality of ui elements.
    """
    def __init__(self, rect: pg.Rect):
        self.visible: bool = True
        self.is_hovered: bool = False
        self.rect: pg.Rect = rect
        self.is_clicked: bool = False
        self.render_needed: bool = True

    def handle_events(
            self, events: List[pg.event.Event], render_context: RenderContext
    ) -> List[pg.event.Event]:
        """
        Handles the given events and updates the element, if needed.
        If a redraw is necessary, sets self.render_needed to True.

        :param events: The events to handle.
        :return: A list of events, that were not handled by this drawable.
        """
        unhandled_events = []
        for event in events:
            if not self.handle_event(event, render_context):
                unhandled_events.append(event)
        self.update(render_context)

        return unhandled_events

    @abstractmethod
    def handle_event(self, event: pg.event.Event, render_context: RenderContext) -> bool:
        """
        Handle an event.

        :param event: The pygame event to handle
        :param render_context: The render context to use for rendering.
        """
        handled = False
        if event.type == pg.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pg.MOUSEBUTTONUP:
            if self.is_hovered:
                self.is_clicked = True
                handled = True

        return handled

    @abstractmethod
    def update(self, render_context: RenderContext):
        """
        Updates the element. Also sets self.render_needed to True, if needed.

        :param render_context: The render context to use for rendering.
        """
        pass

    @final
    def draw(self, screen: pg.Surface, render_context: RenderContext):
        """
        Draw the element to the given screen surface. Do not call this directly. Prefer render().

        :param screen: The screen surface to draw on.
        :param render_context: The render context to use for rendering.
        """
        if self.visible:
            self.render(screen, render_context)
        self.finalize()

    @abstractmethod
    def render(self, screen: pg.Surface, render_context: RenderContext):
        """
        Draw the element to the given screen surface.

        :param screen: The screen surface to draw on.
        :param render_context: The render context to use for rendering.
        """
        pass

    def finalize(self):
        """
        Called at the end of a frame.
        """
        self.is_clicked = False
