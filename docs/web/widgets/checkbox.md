# CheckBox

The `CheckBox` component renders an HTML `<input type="checkbox">`. It is designed for two-way data binding with boolean state variables.

## Usage

Use `bind_checked` to link the checkbox's state to a server-side state variable.

```python
from winup import web

# Create a boolean state variable
notifications_enabled = web.state.create("notifications_enabled", True)
status_text = web.state.create("status_text", "Notifications are currently ON")

async def handle_toggle(event):
    """Update a second state variable based on the checkbox's new state."""
    is_enabled = notifications_enabled.get()
    if is_enabled:
        await status_text.set("Notifications are currently ON")
    else:
        await status_text.set("Notifications are OFF. You will miss important updates.")

@web.component
def Settings():
    return web.ui.Column(children=[
        web.ui.Row(gap="10px", style={'align_items': 'center'}, children=[
            # This checkbox's checked status is bound to the state variable.
            # Its on_change event triggers our handler.
            web.ui.CheckBox(
                bind_checked="notifications_enabled",
                on_change=handle_toggle
            ),
            web.ui.Label("Enable Notifications")
        ]),
        web.ui.Label(
            bind_text="status_text",
            style={'margin_top': '1rem', 'font_style': 'italic'}
        )
    ])
```

## Arguments
- `bind_checked` (str, optional): The key of a boolean state variable to bind the checkbox's `checked` property to. Enables two-way data binding.
- `on_change` (Callable, optional): An `async` or `sync` function that is called when the state of the checkbox changes.
- `props` (dict, optional): A dictionary of additional HTML attributes.
- `**kwargs`: Keyword arguments are also treated as HTML attributes. 