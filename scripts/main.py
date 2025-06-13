#!/usr/bin/env python3
import numpy as np

from viztools.drawable.points import Points
from viztools.render_backend import BackendType
from viztools.render_backend.events import Event, EventType
from viztools.viewer import Viewer

class SimpleViewer(Viewer):
    def __init__(self):
        super().__init__(backend_type=BackendType.PYGAME)
        self.points = Points(
            np.random.normal(size=(200000, 2)) * 5,
            # np.array([[0, 0], [1, 1], [-1, 2]]),
            size=np.random.randint(1, 5, size=200000) ** 2 / 250,
            # size=5,
            color=np.array([0, 255, 0, 50])
        )
        # point types:
        # 0 - normal
        # 1 - hovered
        # 2 - clicked
        self.point_type: np.ndarray = np.zeros(len(self.points), dtype=np.int8)

    def render(self):
        self.render_coordinate_system()
        self.render_drawables([self.points])

    def handle_event(self, event: Event):
        super().handle_event(event)
        if event.type == EventType.MOUSEMOTION:
            clicked_indices = np.nonzero(self.point_type == 2)[0]
            old_hovered = np.nonzero(self.point_type == 1)[0]
            hovered_indices = self.points.hovered_points(self.mouse_pos, self.coordinate_system)
            hovered_indices = np.setdiff1d(hovered_indices, clicked_indices)
            if not np.array_equal(old_hovered, hovered_indices):
                self.point_type[old_hovered] = 0
                self.point_type[hovered_indices] = np.maximum(1, self.point_type[hovered_indices])
                for oh in old_hovered:
                    self.points.set_color(np.array([0, 255, 0, 50]), oh)
                for hi in hovered_indices:
                    self.points.set_color(np.array([0, 255, 0, 100]), hi)
                self.render_needed = True

        if event.type == EventType.MOUSEBUTTONDOWN:
            old_clicked = np.nonzero(self.point_type == 2)[0]
            self.point_type[old_clicked] = 0
            for p_index in old_clicked:
                self.points.set_color(np.array([0, 255, 0, 50]), p_index)

            clicked_indices = self.points.clicked_points(event, self.coordinate_system)
            if len(clicked_indices) > 0:
                self.point_type[clicked_indices] = 2
                for p_index in clicked_indices:
                    self.points.set_color(np.array([255, 0, 0, 50]), p_index)


def main():
    viewer = SimpleViewer()
    viewer.run()


if __name__ == '__main__':
    main()
