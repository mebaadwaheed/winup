# Label

The `Label` component is used to display text. It renders as a `<span>` element by default, but can be configured to render as other elements like `<p>`, `<h1>`, `<h2>`, etc.

## Usage

```python
from winup import web

# A simple text label
web.ui.Label("Hello, World!")

# A label rendered as a main heading
web.ui.Label("This is a Title", tag="h1")

# A label bound to a reactive state variable
status = web.state.create("status", "Connected")
web.ui.Label(bind_text="status")
```

## Arguments

- `text` (str): The text content to display. This is ignored if `bind_text` is used.
- `tag` (str, optional): The HTML tag to use for rendering. Defaults to `"span"`.
- `bind_text` (str, optional): The key of a state variable to bind the label's text to. When the state variable changes, the label's text will automatically update in the browser.
- `props` (dict, optional): A dictionary of additional HTML attributes.
- `**kwargs`: Keyword arguments are also treated as HTML attributes.

## Styling

Apply styles using the `style` prop.

```python
web.ui.Label(
    "Important Notice",
    style={
        'font_weight': 'bold',
        'color': 'red',
        'font_size': '1.2rem'
    }
)
``` 