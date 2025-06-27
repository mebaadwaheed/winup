# Dock

A `Dock` is a panel that can be "docked" to the edges of the main application window, or floated as a separate window. Docks are ideal for tool palettes, inspectors, logs, or navigation trees.

## Usage

You place a `Dock` widget inside your main component's layout. WinUp will automatically find the main window and attach the dock to it.

```python
from winup import ui, winup

@winup.component
def DockExample():
    
    # Content for the dock widget
    dock_content = ui.Column(children=[
        ui.Label("Dock Content"),
        ui.Button("A button"),
        ui.Checkbox("A checkbox")
    ])

    # The main content for the window's central area
    main_content = ui.Label("This is the central widget.")

    return ui.Row(children=[
        # The Dock itself is a container
        ui.Dock(
            children=dock_content,
            props={
                "title": "My Tools",
                "area": "left",
                "allowed_areas": ["left", "right"]
            }
        ),
        main_content
    ])

```

## How It Works

The `ui.Dock` component you create is a placeholder in your layout. When it's first shown, it creates a `QDockWidget` (the real dock panel) and adds it to your application's `QMainWindow`. This allows you to define your docks declaratively as part of your component tree.

## Constructor Parameters

- `children: list`: A list of widgets to be placed inside the dock panel.
- `props: dict` (optional): A dictionary to configure the dock's behavior.

## Special Properties

You can pass these special keys inside the `props` dictionary:

- `title: str`: The text that appears in the dock's title bar.
- `area: str`: The initial area where the dock should appear. Can be `"left"`, `"right"`, `"top"`, or `"bottom"`. Defaults to `"left"`.
- `allowed_areas: List[str]`: A list of areas where the user is allowed to drag and drop the dock. The list can contain `"left"`, `"right"`, `"top"`, `"bottom"`, or `"all"`.

## Methods

### `.add_child(child: QWidget)`
Adds a widget to the dock's content area after it has been created. 