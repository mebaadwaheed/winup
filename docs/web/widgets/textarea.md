# TextArea

The `TextArea` component renders a multi-line HTML `<textarea>` element. Like the `Input` component, it is designed for two-way data binding.

## Usage

Use `TextArea` for collecting longer-form text from users. It shares the same `bind_value` mechanism as `Input`.

```python
from winup import web

# Create a state variable to hold the content
user_bio = web.state.create("user_bio", "This is my default bio.")

@web.component
def BioEditor():
    return web.ui.Column(children=[
        web.ui.Label("Edit your bio:"),
        
        # This textarea has two-way binding with the "user_bio" state.
        web.ui.TextArea(
            bind_value="user_bio",
            style={'width': '100%', 'height': '150px'}
        ),
        
        web.ui.Label("Preview:", style={'margin_top': '1rem', 'font_weight': 'bold'}),
        web.ui.Label(bind_text="user_bio")
    ])
```

## Arguments
- `initial_text` (str): The initial text content of the textarea. This is ignored if `bind_value` is used.
- `bind_value` (str, optional): The key of a state variable to bind the textarea's value to. This enables two-way data binding.
- `props` (dict, optional): A dictionary of additional HTML attributes (e.g., `rows`, `cols`).
- `**kwargs`: Keyword arguments are also treated as HTML attributes. 