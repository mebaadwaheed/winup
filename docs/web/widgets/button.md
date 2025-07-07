# Button

The `Button` component renders a standard HTML `<button>` element. It's one of the primary ways to trigger events in your application.

## Usage

```python
from winup import web

async def handle_click(event):
    print("Button was clicked!")
    # You can update state here
    # await web.state.set("my_state", new_value)

@web.component
def ButtonDemo():
    return web.ui.Button(
        "Click Me",
        on_click=handle_click,
        style={
            'background_color': 'blue',
            'color': 'white',
            'padding': '10px 20px',
            'border_radius': '5px'
        }
    )
```

## Arguments

- `text` (str): The text to display inside the button.
- `on_click` (Callable, optional): An `async` or `sync` function to be called when the button is clicked. It receives a single `event` argument.
- `props` (dict, optional): A dictionary of additional HTML attributes to apply to the button element.
- `**kwargs`: Keyword arguments are also treated as HTML attributes. For example, `disabled=True` will render a disabled button.

## Styling

You can style the button by passing a dictionary of CSS properties to the `style` key within the `props` dictionary or directly as a `style` keyword argument. Remember to use `snake_case` for CSS property names (e.g., `background_color`), which will be automatically converted to `camelCase` (`backgroundColor`) for the browser. 