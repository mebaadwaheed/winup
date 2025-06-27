# Slider

A `Slider` allows the user to select a value from a specified range by dragging a handle along a track.

## Usage

```python
from winup import ui

@winup.component
def SliderExample():
    def on_slider_change(value):
        print(f"Slider value: {value}")

    return ui.Column(children=[
        # A simple horizontal slider
        ui.Slider(min=0, max=100, value=50, on_change=on_slider_change),

        # A vertical slider with a custom track color
        ui.Slider(
            min=0,
            max=255,
            horizontal=False,
            track_color="#33aaff"
        ),

        # A slider with a fully custom thumb style
        ui.Slider(
            min=0,
            max=10,
            value=2,
            thumb_style={
                "background": "red",
                "border-radius": "0px", # Make it square
                "width": "10px",
                "height": "20px"
            }
        )
    ])
```

## Constructor Parameters

- `min: int`: The minimum value of the slider. Defaults to `0`.
- `max: int`: The maximum value of the slider. Defaults to `100`.
- `step: int`: The step size for keyboard interactions. Defaults to `1`.
- `value: int`: The initial value of the slider. Defaults to `0`.
- `on_change: callable` (optional): A function to call when the slider's value changes. It receives the new integer value as its only argument.
- `horizontal: bool`: If `True`, the slider is horizontal; otherwise, it's vertical. Defaults to `True`.
- `track_color: str` (optional): A CSS color string (e.g., `#ff0000`, `"blue"`) for the slider's track.
- `thumb_style: dict` (optional): A dictionary of QSS properties to style the slider's handle (thumb).

## Methods

### `.get_value() -> int`
Returns the current integer value of the slider.

### `.set_value(value: int)`
Programmatically sets the value of the slider. 