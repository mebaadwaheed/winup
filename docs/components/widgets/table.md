# Table Widget

The Table widget provides a way to display and interact with tabular data in your WinUp application.

## Basic Usage

```python
import winup
from winup import ui

@winup.component
def TableDemo():
    headers = ["Name", "Age", "City"]
    data = [
        ["John Doe", "30", "New York"],
        ["Jane Smith", "25", "London"],
        ["Bob Johnson", "35", "Paris"]
    ]
    
    return ui.Table(
        headers=headers,
        data=data,
        props={
            "margin": "10px",
            "min-width": "400px"
        }
    )
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| headers | List[str] | Column headers for the table |
| data | List[List[str]] | 2D array of table data |
| on_cell_clicked | Callable[[int, int], None] | Callback when a cell is clicked |
| on_selection_changed | Callable[[], None] | Callback when selection changes |

## Methods

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| set_data | data: List[List[str]] | None | Updates table data |
| set_headers | headers: List[str] | None | Updates table headers |
| get_selected_cells | None | List[tuple] | Returns list of selected (row, col) |
| get_cell_value | row: int, column: int | str | Gets value of specific cell |
| set_cell_value | row: int, column: int, value: str | None | Sets value of specific cell |
| clear_selection | None | None | Clears current selection |
| clear_contents | None | None | Clears all data |

## Advanced Example

```python
import winup
from winup import ui

@winup.component
def AdvancedTableDemo():
    def on_cell_click(row: int, col: int):
        print(f"Cell clicked: ({row}, {col})")
        value = table.get_cell_value(row, col)
        print(f"Value: {value}")
    
    def on_selection():
        selected = table.get_selected_cells()
        print(f"Selected cells: {selected}")
    
    headers = ["ID", "Product", "Price"]
    data = [
        ["1", "Widget", "$10.00"],
        ["2", "Gadget", "$15.00"],
        ["3", "Tool", "$20.00"]
    ]
    
    table = ui.Table(
        headers=headers,
        data=data,
        on_cell_clicked=on_cell_click,
        on_selection_changed=on_selection,
        props={
            "margin": "10px",
            "min-width": "500px",
            "min-height": "300px"
        }
    )
    
    return table

# Run the demo
if __name__ == "__main__":
    winup.run(
        main_component_path="your_module:AdvancedTableDemo",
        title="Advanced Table Demo",
        width=600,
        height=400
    )
```

## Styling

The Table widget supports all standard WinUp styling properties. Some commonly used ones include:

```python
props = {
    "margin": "10px",
    "min-width": "400px",
    "min-height": "300px",
    "background-color": "#ffffff",
    "border": "1px solid #ddd",
    "border-radius": "4px"
}
```

## Notes

- All data is stored as strings internally. If you need to work with numbers, convert them as needed.
- The table automatically resizes columns to fit content.
- Multiple cell selection is enabled by default. 