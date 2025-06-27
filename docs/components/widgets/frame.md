# Frame

A `Frame` is the most fundamental container widget in WinUp. It's essentially a blank panel that can hold other widgets. It can be styled and can manage the layout of its children.

## Usage

Frames are used to group, contain, and style other components.

```python
from winup import ui, winup

@winup.component
def FrameExample():
    return ui.Frame(
        # A Frame defaults to a vertical layout (VBox)
        children=[
            ui.Label("This is inside a frame."),
            ui.Button("Button 1"),
            ui.Button("Button 2")
        ],
        props={
            "background-color": "#f0f0f0",
            "border": "2px solid #ccc",
            "border-radius": "10px",
            "padding": "15px"
        }
    )
```

## Layouts

A `Frame` can use any of Qt's layout managers. You can specify the layout using the `layout` prop.

```python
from winup.ui import layout_managers as lm

# A Frame with a horizontal layout
horizontal_frame = ui.Frame(
    layout=lm.HBox(spacing=20),
    children=[...],
    props={"background-color": "lightblue"}
)

# You can also use string shortcuts for simple box layouts
vertical_frame = ui.Frame(layout="vertical", children=[...])
horizontal_frame_2 = ui.Frame(layout="horizontal", children=[...])
```

## Constructor Parameters

- `children: list` (optional): A list of child widgets to be placed inside the `Frame`.
- `props: dict` (optional): A dictionary of style properties and special properties.
- `**kwargs`: Any additional keyword arguments are also treated as style properties.

## Special Properties

You can pass these special keys inside the `props` dictionary:

- `layout`: An instance of a layout manager (e.g., `VBox()`, `HBox()`, `QGridLayout()`). Can also be the string `"vertical"` or `"horizontal"`. If not provided, a `VBox` is created automatically when children are added.
- `on_mount: callable`: A function to be called once, the first time the `Frame` is shown on screen.
- `on_unmount: callable`: A function to be called when the `Frame` is closed.

## Methods

### `.set_layout(layout)`
Sets or changes the layout manager for the `Frame`.

### `.add_child(child: QWidget, stretch: int = 0)`
Adds a single child widget to the `Frame`'s layout.

### `.add_children(children: list)`
Adds a list of child widgets to the `Frame`'s layout. 