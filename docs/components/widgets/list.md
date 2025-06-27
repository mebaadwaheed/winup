# List

The `List` widget displays a vertical list of items. It supports single or multiple selection, and can be displayed as an ordered (numbered) or unordered list.

## Usage

```python
from winup import ui, state

def ListExample():
    # State to hold the selected item
    selected_item = state.create("list_selection", "None")

    return ui.Row(props={"spacing": 20}, children=[
        # An ordered, single-selection list
        ui.Column(children=[
            ui.Label("Single-Select Ordered List"),
            ui.List(
                items=["Apple", "Banana", "Cherry"],
                ordered=True,
                on_select=lambda item: selected_item.set(item),
                width=200
            ),
            ui.Label(text=selected_item.get())
        ]),

        # An unordered, multi-selection list
        ui.Column(children=[
            ui.Label("Multi-Select List"),
            ui.List(
                items=["Python", "JavaScript", "C++", "Rust"],
                multi_select=True,
                on_select=lambda items: print(f"Selected languages: {items}"),
                width=200
            )
        ])
    ])
```

## Constructor Parameters

- `items: list[str]`: **Required**. The list of strings to display in the list.
- `selected_index: int` (optional): The index of the item to be selected initially. Defaults to `None`.
- `on_select: callable` (optional): A callback function that is triggered when an item is selected.
  - In single-select mode, it receives the selected item's string.
  - In multi-select mode, it receives a list of the selected items' strings.
- `multi_select: bool` (optional): If `True`, allows the user to select multiple items. Defaults to `False`.
- `ordered: bool` (optional): If `True`, prefixes each item with its number (e.g., "1. Apple"). Defaults to `False`.
- `disabled: bool` (optional): If `True`, the widget will be disabled. Defaults to `False`.
- `height: int` (optional): A fixed height for the widget in pixels.
- `width: int` (optional): A fixed width for the widget in pixels.
- `style: dict` (optional): A dictionary of QSS properties for custom styling.
- `id: str` (optional): A unique identifier for the widget.
- `className: str` (optional): A string of space-separated class names for styling. 