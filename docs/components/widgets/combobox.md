# ComboBox

A `ComboBox` is a dropdown menu that allows users to select one option from a list.

## Usage

```python
from winup import ui, winup

@winup.component
def ComboBoxExample():
    items = ["Option 1", "Option 2", "Option 3", "Another Choice"]

    def on_selection_change(selected_text):
        print(f"Selected: {selected_text}")

    return ui.Column(children=[
        ui.Label(text="Please select an option:"),
        ui.ComboBox(items=items, on_change=on_selection_change)
    ])
```

## Constructor Parameters

- `items: List[str]`: A list of strings that will populate the dropdown options.
- `on_change: callable` (optional): A function to call when the selected item changes. It receives the text of the newly selected item as its only argument.
- `props: dict` (optional): A dictionary of style properties to apply to the `ComboBox`.

## Methods

The `ComboBox` inherits all methods from `QComboBox`, including:

- `.currentText() -> str`: Returns the text of the currently selected item.
- `.setCurrentText(text: str)`: Programmatically selects an item by its text.
- `.addItem(text: str)`: Adds a new item to the end of the list.
- `.addItems(texts: List[str])`: Adds multiple new items to the end of the list.
- `.clear()`: Removes all items from the list.
- `.count() -> int`: Returns the number of items in the list. 