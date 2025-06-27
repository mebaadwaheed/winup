# RadioButton

A `RadioButton` is used to select one option from a set of mutually exclusive choices. Radio buttons are typically used in groups; only one button in a group can be selected at a time.

To group radio buttons, simply make them children of the same parent layout component (like a `Column` or `Row`). WinUp handles the grouping automatically.

## Usage

```python
from winup import ui

@winup.component
def RadioButtonExample():
    def on_option_toggled(is_checked, option_name):
        if is_checked:
            print(f"Selected option: {option_name}")

    return ui.Column(children=[
        ui.Label(text="Choose a shipping method:"),
        ui.RadioButton(
            text="Standard (5-7 days)",
            on_toggle=lambda checked: on_option_toggled(checked, "Standard")
        ).set_checked(True), # Pre-select the first option
        
        ui.RadioButton(
            text="Express (2-3 days)",
            on_toggle=lambda checked: on_option_toggled(checked, "Express")
        ),
        
        ui.RadioButton(
            text="Overnight (1 day)",
            on_toggle=lambda checked: on_option_toggled(checked, "Overnight")
        )
    ])
```

## Constructor Parameters

- `text: str`: The label to be displayed next to the radio button.
- `props: dict` (optional): A dictionary of style properties.
- `on_toggle: callable` (optional): A function to be called when the radio button's state changes. It receives a boolean argument indicating if the button has been toggled *on* (`True`).

## Methods

### `.on_toggle(func: callable)`
A chainable method to set the toggle handler.

### `.is_checked() -> bool`
Returns `True` if the radio button is currently selected.

### `.set_checked(checked: bool)`
A chainable method to programmatically select or deselect the radio button. 