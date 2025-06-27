# Switch

The `Switch` is a binary toggle widget, visually represented as a modern "on/off" switch. Functionally, it is identical to a `Checkbox`, but provides a different aesthetic.

## Usage

```python
from winup import ui

@winup.component
def SwitchExample():
    def on_toggle(is_on):
        print(f"The switch is now {'ON' if is_on else 'OFF'}")

    return ui.Column(children=[
        # A simple switch with a label
        ui.Switch(text="Enable Notifications"),

        # A switch with a toggle handler, defaulted to 'on'
        ui.Switch(
            text="Dark Mode",
            is_checked=True,
            on_toggle=on_toggle
        )
    ])
```

## Constructor Parameters

- `text: str`: The label to be displayed next to the switch.
- `is_checked: bool`: The initial state of the switch. `True` is "on", `False` is "off". Defaults to `False`.
- `on_toggle: callable` (optional): A function to be called when the switch's state changes. It receives the new boolean state as its only argument.
- `props: dict` (optional): A dictionary of style properties. Note that the core visual style of the switch is handled by a built-in stylesheet and may not be fully overridable with props.

## Methods

The `Switch` widget inherits all the methods from `Checkbox`, including:

- `.on_toggle(func: callable)`
- `.is_checked() -> bool`
- `.set_checked(checked: bool)` 