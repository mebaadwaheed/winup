# TextArea

The `TextArea` widget is a multi-line text field, suitable for capturing longer form text from a user. It is a wrapper around Qt's `QTextEdit`.

## Usage

```python
from winup import ui, winup

@winup.component
def TextAreaExample():
    return ui.Column(children=[
        # A simple textarea with a placeholder
        ui.TextArea(placeholder="Enter a long description here..."),

        # A styled textarea with initial text
        ui.TextArea(
            text="This is some initial content.",
            props={
                "border": "1px solid #ccc",
                "border-radius": "5px",
                "font-size": "14px",
                "background-color": "#f9f9f9"
            }
        )
    ])
```

## Constructor Parameters

- `placeholder: str`: The placeholder text to display when the `TextArea` is empty.
- `text: str`: The initial text value.
- `props: dict` (optional): A dictionary of style properties to apply.

## Methods

The `TextArea` widget inherits all methods from `QTextEdit`, including:

- `.setPlainText(text: str)`: Sets the content of the `TextArea`.
- `.toPlainText() -> str`: Returns the content of the `TextArea` as a string.
- `.clear()`: Clears all text.
- `.setReadOnly(is_read_only: bool)`: Makes the `TextArea` editable or read-only. 