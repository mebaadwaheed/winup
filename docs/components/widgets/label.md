# Label

The `Label` widget is used to display non-editable text or images. It's one of the most common widgets for displaying information to the user.

## Usage

```python
from winup import ui, winup

@winup.component
def LabelExample():
    return ui.Column(children=[
        # A simple text label
        ui.Label(text="Hello, World!"),

        # A bold label using the convenience parameter
        ui.Label(text="This is bold text.", bold=True),

        # A label with a larger font size
        ui.Label(text="This text is larger.", font_size=24),

        # A styled label using props
        ui.Label(
            text="Styled Label",
            props={
                "color": "purple",
                "font-size": "18px",
                "font-style": "italic"
            }
        )
    ])
```

## Constructor Parameters

- `text: str`: The text to be displayed by the label. Defaults to `""`.
- `props: dict` (optional): A dictionary of style properties to apply to the label.
- `bold: bool`: A convenience parameter to make the text bold. Sets `font-weight: bold`. Defaults to `False`.
- `font_size: int`: A convenience parameter to set the font size in pixels.

## Methods

### `.set_text(text: str)`

A Pythonic alias for Qt's `setText()` method. It updates the text of the label after it has been created.

```python
my_label = ui.Label("Initial text")

# Sometime later...
my_label.set_text("Updated text")
``` 