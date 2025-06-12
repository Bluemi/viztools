from enum import StrEnum

import numpy as np


class EventType(StrEnum):
    QUIT = 'QUIT'
    KEYDOWN = 'KEYDOWN'
    KEYUP = 'KEYUP'
    MOUSEBUTTONDOWN = 'MOUSEBUTTONDOWN'
    MOUSEBUTTONUP = 'MOUSEBUTTONUP'
    MOUSEMOTION = 'MOUSEMOTION'
    WINDOWENTER = 'WINDOWENTER'
    WINDOWFOCUSGAINED = 'WINDOWFOCUSGAINED'
    WINDOWRESIZED = 'WINDOWRESIZED'
    MOUSEWHEEL = 'MOUSEWHEEL'


class Event:
    def __init__(self, event_type: EventType):
        self.type = event_type


class MouseMotionEvent(Event):
    def __init__(self, pos: np.ndarray, rel: np.ndarray):
        super().__init__(EventType.MOUSEMOTION)
        self.pos = pos
        self.rel = rel


class MouseWheelEvent(Event):
    def __init__(self, scroll: int):
        super().__init__(EventType.MOUSEWHEEL)
        self.scroll = scroll


class MouseButtonDownEvent(Event):
    def __init__(self, button: int, pos: np.ndarray):
        super().__init__(EventType.MOUSEBUTTONDOWN)
        self.button = button
        self.pos = pos
