# ScrollView

A `ScrollView` provides a scrollable view for a single child widget. It's essential for displaying content that might be larger than the available screen space, such as long lists, text documents, or large images.

## Usage

A `ScrollView` takes a single widget as its `child`. This child is typically a `Column` or `Row` that contains the actual list of items.

```python
from winup import ui, winup

@winup.component
def ScrollViewExample():
    # Create a column to hold the scrollable content
    content = ui.Column(spacing=10)

    # Add a large number of widgets to the column
    for i in range(50):
        content.add_child(ui.Label(f"Item number {i + 1}"))

    # Place the column inside the ScrollView
    return ui.ScrollView(child=content, props={"height": "300px"})
```

## Constructor Parameters

- `child: QWidget`: The single widget to be placed inside the scrollable area. This is most often a `Column` or `Row`.
- `props: dict` (optional): A dictionary of style properties to apply to the `ScrollView` container itself (e.g., `height`, `border`).

## Methods

### `.scroll_to_bottom()`
Programmatically scrolls the view to the very bottom of its content. This is useful for chat applications or logs where you want to show the most recent item.

### `.add_child(widget: QWidget)`
A convenience method that adds a widget directly to the `ScrollView`'s content widget. This requires the content widget to have its own `add_child` method (like `Frame`, `Column`, or `Row`).

### `.set_widget(widget: QWidget)`
Replaces the current content widget with a new one. 