# ColorPicker

The `ColorPicker` widget allows users to select a color from a standard system dialog. It displays the currently selected color as its background.

## Usage

```python
from winup import ui, state, style

def ColorPickerExample():
    # Create a state object to hold the selected color
    selected_color = state.create("selected_color", "#ff0000")

    # Define a handler to update the state when the color changes
    def handle_color_change(new_color):
        selected_color.set(new_color)

    # A label whose text color is bound to the state
    display_label = ui.Label()
    selected_color.bind_to(display_label, 'style', lambda c: {"color": c, "font-size": "20px"})
    selected_color.bind_to(display_label, 'text', lambda c: f"This text is now the color {c}")

    return ui.Column(props={"spacing": 10}, children=[
        ui.ColorPicker(
            selected_color=selected_color.get(),
            on_change=handle_color_change,
            enable_alpha=True,
            preset_colors=["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]
        ),
        display_label
    ])
```

## Constructor Parameters

- `selected_color: str`: **Required**. The initial color to display, in a format like `"#RRGGBB"`, `"#AARRGGBB"`, or a color name.
- `on_change: callable` (optional): A callback function that is triggered when the user selects a new color. It receives the new color string as its only argument.
- `enable_alpha: bool` (optional): If `True`, the color dialog will allow the user to select the alpha (transparency) channel. Defaults to `False`.
- `preset_colors: list[str]` (optional): A list of color strings to show as custom preset swatches in the color dialog.
- `disabled: bool` (optional): If `True`, the widget will be disabled and cannot be interacted with. Defaults to `False`.
- `style: dict` (optional): A dictionary of QSS properties to apply custom styles to the widget.
- `id: str` (optional): A unique identifier for the widget, used for styling with ID selectors.
- `className: str` (optional): A string of space-separated class names for applying styles with class selectors. 