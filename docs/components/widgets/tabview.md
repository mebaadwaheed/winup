# TabView

A `TabView` is a container that presents different widgets in a stack, with tabs at the top allowing the user to switch between them.

## Usage

You create a `TabView` by passing it a dictionary where the keys are the tab titles (strings) and the values are the widget components to display in each tab's content area.

```python
from winup import ui, winup

@winup.component
def TabViewExample():
    # Define the content for each tab
    tab1_content = ui.Column(children=[
        ui.Label("This is the content for the first tab."),
        ui.Button("A button")
    ])

    tab2_content = ui.Image(src="path/to/image.png")

    tab3_content = ui.Label("Just some text for the third tab.")

    # Create the dictionary of tabs
    my_tabs = {
        "First Tab": tab1_content,
        "An Image": tab2_content,
        "Third": tab3_content
    }

    return ui.TabView(tabs=my_tabs)
```

## Constructor Parameters

- `tabs: Dict[str, QWidget]`: A dictionary mapping tab titles to the widgets that will be the content of each tab.
- `props: dict` (optional): A dictionary of style properties to apply to the `TabView` container.

## Methods

### `.add_tab(widget: QWidget, label: str)`
Programmatically adds a new tab to the `TabView` after it has been created.

The `TabView` also inherits all methods from `QTabWidget`, such as:

- `.setCurrentIndex(index: int)`: Selects a tab by its numerical index.
- `.currentIndex() -> int`: Returns the index of the currently selected tab.
- `.count() -> int`: Returns the total number of tabs. 