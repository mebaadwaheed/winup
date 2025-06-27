# ExpandablePanel

An `ExpandablePanel` is a widget that can be collapsed to hide its content, showing only a header. Clicking the header toggles the visibility of the content area with a smooth slide animation. This is useful for creating accordions, FAQs, or hiding advanced settings.

## Usage

```python
from winup import ui, winup

@winup.component
def ExpandablePanelExample():
    
    # Define the content for the panel
    panel_content = ui.Column(children=[
        ui.Label("This is the hidden content."),
        ui.Checkbox("An option"),
        ui.Input(placeholder="Another widget")
    ])

    return ui.Column(children=[
        ui.ExpandablePanel(
            title="Click to Expand Me",
            children=panel_content
        ),
        ui.ExpandablePanel(
            title="This One Starts Expanded",
            children=[ui.Label("Some more content here...")],
            expanded=True,
            header_props={"background-color": "#e0e0e0"}
        )
    ])
```

## Constructor Parameters

- `title: str`: The text to display in the header.
- `children: list` (optional): A list of widgets to be placed inside the collapsible content area.
- `expanded: bool`: If `True`, the panel will be expanded by default. Defaults to `False`.
- `animation_duration: int`: The duration of the expand/collapse animation in milliseconds. Defaults to `300`.
- `header_props: dict` (optional): A dictionary of style properties to apply to the header button.
- `content_props: dict` (optional): A dictionary of style properties to apply to the content area `Frame`.
- `expand_icon: str`: The character or string to show next to the title when the panel is expanded. Defaults to `"▼"`.
- `collapse_icon: str`: The character or string to show when the panel is collapsed. Defaults to `"►"`.

## Methods

### `.add_child(widget: QWidget)`
Adds a new widget to the content area.

### `.setContent(widget: QWidget)`
Replaces the entire content of the panel with a new single widget.

### `.expand()`
Programmatically expands the panel.

### `.collapse()`
Programmatically collapses the panel.

### `.set_animation_duration(msecs: int)`
Changes the animation duration.

## Events

### `.animationFinished`
A Qt Signal that is emitted when the expand or collapse animation completes. 