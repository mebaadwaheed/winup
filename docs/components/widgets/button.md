# Button

The `Button` widget is a standard clickable button that users can interact with to trigger actions.

## Usage

```python
from winup import ui, winup

@winup.component
def ButtonExample():
    def handle_click():
        print("Button was clicked!")

    return ui.Column(children=[
        # A simple button with a click handler
        ui.Button(text="Click Me", on_click=handle_click),

        # A styled button using props
        ui.Button(
            text="Styled Button",
            props={
                "background-color": "blue",
                "color": "white",
                "border-radius": "8px",
                "padding": "10px"
            }
        ),

        # A button with an icon
        ui.Button(text="Icon Button").set_icon("path/to/icon.svg", size=20, color="white")
    ])
```

## Constructor Parameters

- `text: str`: The text displayed on the button. Defaults to `"Button"`.
- `props: dict` (optional): A dictionary of style properties to apply to the button.
- `on_click: callable` (optional): A function to be called when the button is clicked.
- `on_click_enabled: bool`: If `False`, the `on_click` handler will not be attached. Defaults to `True`.

## Methods

### `.on_click(func: callable)`

A chainable method to set the click handler for the button. This is an alternative to the `on_click` constructor parameter and will replace any existing handler.

```python
my_button = ui.Button("Click me")
my_button.on_click(lambda: print("New handler!"))
```

### `.set_icon(icon_path: str, size: int = 16, color: str = None)`

A chainable method to set an icon on the button.

- `icon_path`: The file path to the icon image (e.g., `.svg`, `.png`).
- `size`: The size of the icon in pixels.
- `color`: An optional hex or color name string (e.g., `"#FFFFFF"`, `"white"`). If provided, WinUp will attempt to recolor the icon. This works best with simple, single-color icons (like SVGs or black PNGs). 