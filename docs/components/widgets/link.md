# Link

The `Link` widget displays text that acts as a hyperlink. When clicked, it will open the specified URL in the user's default web browser.

## Usage

```python
from winup import ui, winup

@winup.component
def LinkExample():
    return ui.Column(children=[
        ui.Link(text="Visit the WinUp GitHub page", url="https://github.com/mebaadwaheed/winup"),
        
        # This will open the URL in 5 separate browser tabs when clicked.
        ui.Link(text="Open 5 tabs to Google", url="https://google.com", tabs=5)
    ])
```

## Constructor Parameters

- `text: str`: The clickable text to be displayed.
- `url: str`: The URL that will be opened when the link is clicked.
- `tabs: int`: The number of browser tabs to open when the link is clicked. Defaults to `1`. This can be useful for testing or for specific application needs, but be mindful of the user experience.

## Styling

The `Link` widget comes with default styling to make it look like a standard web link (blue, with an underline on hover). You can override these styles by passing a `props` dictionary with your own QSS properties, just like with other widgets. 