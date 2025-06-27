# Deck

A `Deck` is a container that stacks multiple child widgets on top of each other, but only shows one at a time. It is the fundamental building block for creating multi-page interfaces, wizards, and is used internally by the `Router`.

Think of it as a deck of cards, where you can only see the top card.

## Usage

You provide a `Deck` with a list of children. The currently visible child is controlled by its index.

```python
from winup import ui, winup

@winup.component
def DeckExample():
    # Define the pages (widgets) for our deck
    page1 = ui.Label("This is the first page.")
    page2 = ui.Image(src="path/to/image.png")
    page3 = ui.Column(children=[
        ui.Label("This is the third page."),
        ui.Button("A button")
    ])

    my_deck = ui.Deck(children=[page1, page2, page3])

    # Buttons to control which page is visible
    controls = ui.Row(children=[
        ui.Button("Show Page 1", on_click=lambda: my_deck.setCurrentIndex(0)),
        ui.Button("Show Page 2", on_click=lambda: my_deck.setCurrentIndex(1)),
        ui.Button("Show Page 3", on_click=lambda: my_deck.setCurrentIndex(2))
    ])

    return ui.Column(children=[
        controls,
        my_deck
    ])
```

## Constructor Parameters

- `children: list`: A list of widgets to be added to the `Deck`. The order of the list determines the index of each widget.
- `props: dict` (optional): A dictionary of style properties to apply to the `Deck` container.

## Methods

The `Deck` inherits all methods from `QStackedWidget`, the most important of which are:

### `.setCurrentIndex(index: int)`
Changes the visible widget to the one at the specified index.

### `.currentIndex() -> int`
Returns the index of the currently visible widget.

### `.addWidget(widget: QWidget)`
Adds a new widget to the end of the stack.

### `.widget(index: int) -> QWidget`
Returns the widget at the specified index.

### `.count() -> int`
Returns the total number of widgets in the stack. 