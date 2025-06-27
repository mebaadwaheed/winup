# TreeView

The `TreeView` widget is used to display hierarchical data in a tree structure, like a file explorer.

## Usage

```python
from winup import ui, state

def TreeViewExample():
    # The hierarchical data structure
    file_system = {
        "Documents": {
            "Work": {"Report.docx": {}, "Presentation.pptx": {}},
            "Personal": {"todos.txt": {}}
        },
        "Pictures": {
            "Vacation": {"photo1.jpg": {}, "photo2.jpg": {}},
            "Family": {}
        }
    }

    # State for the selected and expanded nodes
    selected_node = state.create("tree_selection", "Documents.Work.Report.docx")
    expanded_nodes = state.create("tree_expanded", {"Documents", "Pictures.Vacation"})

    return ui.Column(props={"spacing": 5}, children=[
        ui.Label("File Explorer"),
        ui.TreeView(
            data=file_system,
            selected_node=selected_node.get(),
            expanded_nodes=expanded_nodes.get(),
            on_select=lambda key: selected_node.set(key),
            on_expand=lambda key, expanded: print(f"{key} was {'expanded' if expanded else 'collapsed'}"),
            width=300,
            height=250
        ),
        ui.Label(text=selected_node.bind_to(lambda s: f"Selected: {s}"))
    ])
```

## Constructor Parameters

- `data: dict`: **Required**. A nested dictionary representing the tree structure. Keys are the node names, and values are other dictionaries for child nodes. An empty dictionary signifies a leaf node.
- `expanded_nodes: set` (optional): A set of node keys that should be expanded by default. A node key is a dot-separated path from the root (e.g., `"root.parent.child"`).
- `selected_node: str` (optional): The key of the node that should be selected by default.
- `on_select: callable` (optional): A callback function that is triggered when a node is selected. It receives the selected node's key as its argument.
- `on_expand: callable` (optional): A callback that is triggered when a node is expanded or collapsed. It receives the node's key and a boolean (`True` for expanded, `False` for collapsed).
- `show_icons: bool` (optional): If `True`, shows default folder/file icons next to nodes. Currently not implemented. Defaults to `True`.
- `height: int` (optional): A fixed height for the widget in pixels.
- `width: int` (optional): A fixed width for the widget in pixels.
- `style: dict` (optional): A dictionary of QSS properties for custom styling.
- `id: str` (optional): A unique identifier for the widget.
- `className: str` (optional): A string of space-separated class names for styling. 