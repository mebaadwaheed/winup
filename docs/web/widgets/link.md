# Link

The `Link` component renders a standard hyperlink (`<a>` tag). It's used for navigation to internal or external pages.

## Usage

```python
from winup import web

@web.component
def Navigation():
    return web.ui.Row(gap="20px", children=[
        # A simple internal link
        web.ui.Link("Home", href="/"),
        
        # A link to an external site that opens in a new tab
        web.ui.Link(
            "Visit Python.org",
            href="https://www.python.org",
            props={'target': '_blank'}
        ),
        
        # A styled link
        web.ui.Link(
            "Dashboard",
            href="/dashboard",
            style={'color': 'magenta', 'text_decoration': 'none'}
        )
    ])
```

## Arguments
- `text` (str): The visible text for the link.
- `href` (str): The URL that the link points to. Defaults to `"#`.
- `props` (dict, optional): A dictionary of additional HTML attributes (e.g., `target`, `rel`).
- `**kwargs`: Keyword arguments are also treated as HTML attributes. 