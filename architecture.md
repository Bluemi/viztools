from viztools.utils import RenderContext

# Architecture

## Drawables
Drawables are items drawn to the canvas. Examples include Lines, Points, Images and Labels.
The position and size is defined relative to a coordinate system, that can change by mouse or keyboard actions.

### Using drawables
A minimalistic example could look like this:
```python
import pygame
import numpy as np
from viztools.drawable.points import Points
from viztools.coordinate_system import CoordinateSystem
from viztools.utils import RenderContext

screen = pygame.display.set_mode((800, 600))
coordinate_system = CoordinateSystem(screen.get_size())
render_context = RenderContext.default()

drawable = Points(np.array([[0.0, 0.0], [1.0, 0.0]]))
while True:
    drawable.handle_events(pygame.event.get(), screen, coordinate_system, render_context)
    drawable.draw(screen, coordinate_system, render_context)
```
*Note: In order to make the coordinate system move, you would need a controller for the coordinate system as well. In practice use a viewer class for ease of use.*

Drawables are created simply by their `__init__()` method.

Drawables expose a small interface via their methods:

### The `handle_events()` method
The method `Drawable.handle_events(events: List[pygame.event.Event], screen: pygame.Surface, coordinate_system: CoordinateSystem, render_context: RenderContext)` takes a list of events,
applies those to the element and returns a new list, containing all unhandled events.
Each element should only be called once per frame.

### The `draw()` method
To draw an element to the screen use the `Drawable.draw(screen: pygame.Surface, coordinate_system: CoordinateSystem, render_context: RenderContext)` method.
It will just do that ;).

### Internal architecture
The normal flow of method calls of a Drawable will be this:
```
- handle_events()
  - handle_event() <- abstract
  - update() <- abstract
- draw()
  - render() <- abstract
  - finalize() <- can be overwritten
```

## UI elements
UI elements are items drawn to a static position on the screen (they do not react to changes of the coordinate system).

They have a similar interface to Drawables.

### The `handle_events()` method
The method `UIElement.handle_events(events: List[pygame.event.Event], render_context: RenderContext)` takes a list of events,
applies those to the element and returns a new list, containing all unhandled events.
Each element should only be called once per frame.

### The `draw()` method
To draw an ui-element to the screen use the `UIElement.draw(screen: pygame.Surface, render_context: RenderContext)` method.

### Internal architecture
The normal flow of method calls of a `UIElements` will be this:
```
- handle_events()
  - handle_event() <- abstract
  - update() <- abstract
- draw()
  - render() <- abstract
  - finalize() <- can be overwritten
```
