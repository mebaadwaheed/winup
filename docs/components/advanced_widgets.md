# Advanced Widgets

WinUp also provides more complex, pre-built components for common UI patterns.
For more information read their respective file documentation in the docs/components/widgets folder.

## Dock Widget
The `Dock` widget allows you to create dockable toolbars or panels around a central content area, similar to IDEs or creative software.

*   `position`: Where to place the dock ('left', 'right', 'top', 'bottom').
*   `title`: The title displayed on the dock's title bar.
*   `children`: A list of widgets to place inside the dock area.

```python
import winup
from winup import ui

def App():
    # The central widget can be any component
    central_widget = ui.Label("Main Content Area", props={"alignment": "AlignCenter"})

    # A dockable panel for the left side
    left_dock = ui.Dock(
        position='left',
        title="Tools",
        children=[
            ui.Column([
                ui.Button("Tool 1"),
                ui.Button("Tool 2"),
            ])
        ]
    )
    
    # A dockable panel for the bottom
    bottom_dock = ui.Dock(
        position='bottom',
        title="Logs",
        children=[ui.Textarea("Log messages will appear here...")]
    )

    return ui.Frame(
        children=[left_dock, bottom_dock, central_widget]
    )

# Example: winup.run(main_component_path="dock_demo:App", title="Dock Demo")
```

## Carousel
The `Carousel` widget provides a swipeable, animated container for displaying pages or images.

*   `animation_duration`: Speed of the slide animation in milliseconds.

```python
import winup
from winup import ui

def App():
    return ui.Carousel(
        children=[
            ui.Label("Page 1", props={"background-color": "#f0f0f0", "alignment": "AlignCenter", "height": 150}),
            ui.Label("Page 2", props={"background-color": "#e0e0e0", "alignment": "AlignCenter", "height": 150}),
            ui.Label("Page 3", props={"background-color": "#d0d0d0", "alignment": "AlignCenter", "height": 150}),
        ]
    )

# To run this, you would need a WinUp app instance.
# Example: winup.run(main_component_path="carousel_demo:App", title="Carousel Demo")
```

## Expandable Panel
The `ExpandablePanel` is a container that can be collapsed or expanded by the user, useful for hiding and showing content.

```python
import winup
from winup import ui

def App():
    return ui.ExpandablePanel(
        "Click to Expand",
        children=[
            ui.Column(props={"spacing": 10, "margin": "10px"}, children=[
                ui.Label("This content was hidden!"),
                ui.Input(props={"placeholder": "You can place any widget inside."})
            ])
        ]
    )

# To run this, you would need a WinUp app instance.
# Example: winup.run(main_component_path="expandable_demo:App", title="Expandable Panel Demo")
```