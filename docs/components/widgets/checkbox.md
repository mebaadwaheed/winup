# Checkbox

The `Checkbox` widget allows the user to select a binary "on" or "off" state. It consists of a checkable box and a label.

## Usage

```python
from winup import ui, winup

@winup.component
def CheckboxExample():
    def on_toggle(is_checked):
        print(f"Checkbox state changed to: {is_checked}")

    return ui.Column(children=[
        # A simple checkbox with a label
        ui.Checkbox(text="Enable Feature"),

        # A checkbox with a toggle handler
        ui.Checkbox(
            text="I agree to the terms",
            on_toggle=on_toggle
        ),

        # A pre-checked checkbox
        ui.Checkbox(text="Default is on").set_checked(True)
    ])
```

## Constructor Parameters

- `text: str`: The label to be displayed next to the checkbox.
- `props: dict` (optional): A dictionary of style properties.
- `on_toggle: callable` (optional): A function to be called when the checkbox's state changes. It receives the new boolean state (`True` for checked, `False` for unchecked) as its only argument.

## Methods

### `.on_toggle(func: callable)`
A chainable method to set the toggle handler. This replaces any existing handler.

### `.is_checked() -> bool`
Returns `True` if the checkbox is currently checked, otherwise `False`.

### `.set_checked(checked: bool)`
A chainable method to programmatically set the state of the checkbox. 