# Web Layouts

WinUp for Web uses a component-based layout system heavily inspired by modern web design principles, particularly CSS Flexbox and Grid. This allows you to create complex, responsive UIs by composing simple layout components.

All layout components accept a `children` list and a `props` dictionary for custom styling.

## Column

The `Column` component arranges its children vertically. It is the most common layout component.

- **Maps to**: CSS `display: flex`, `flex-direction: column`.
- **Key Props**:
    - `gap`: The space between children (e.g., `"10px"`, `"1rem"`).
    - `style`: A dictionary for additional CSS properties.

```python
web.ui.Column(
    gap="15px",
    children=[
        web.ui.Label("Top"),
        web.ui.Label("Middle"),
        web.ui.Label("Bottom"),
    ]
)
```

## Row

The `Row` component arranges its children horizontally.

- **Maps to**: CSS `display: flex`, `flex-direction: row`.
- **Key Props**:
    - `gap`: The space between children.
    - `style`: A dictionary for additional CSS properties.

```python
web.ui.Row(
    gap="15px",
    style={'align_items': 'center'}, # Vertically center items in the row
    children=[
        web.ui.Button("Button 1"),
        web.ui.Button("Button 2"),
    ]
)
```

## Grid

The `Grid` component allows for advanced two-dimensional layouts. It gives you precise control over the placement and spanning of child elements.

- **Maps to**: CSS `display: grid`.
- **Child Format**: Children must be provided as tuples in the format `(component, row, col, rowspan, colspan)`.
- **Key Props**:
    - `gap`: The space between grid cells.
    - `grid_template_columns`: Defines the number and width of columns (e.g., `"1fr 1fr 2fr"`, `"repeat(3, 1fr)"`).
    - `grid_template_rows`: Defines the number and height of rows.

```python
web.ui.Grid(
    gap="10px",
    grid_template_columns="repeat(2, 1fr)",
    children=[
        (web.ui.Label("Top Left"),     0, 0, 1, 1),
        (web.ui.Label("Top Right"),    0, 1, 1, 1),
        (web.ui.Label("Bottom Span"),  1, 0, 1, 2), # Spans 2 columns
    ]
)
```

## Stack

The `Stack` component layers its children on top of each other. Only one child is visible at a time. This is useful for creating tabbed views, carousels, or wizard-style navigation where you only show one "page" at a time.

- **Key Props**:
    - `active_child_index`: The index of the child in the `children` list that should be visible. You would typically bind this to a state variable to control which child is shown.

```python
# In a real app, you would have a state variable for the index
# and buttons to change it.
active_page = web.state.create("active_page", 0)

web.ui.Stack(
    active_child_index=active_page.get(), # Or bind it
    children=[
        PageOneComponent(),
        PageTwoComponent(),
    ]
)
```

## Flex

The `Flex` component is a more generic version of `Row` and `Column` that provides direct access to all of CSS Flexbox's properties.

- **Key Props**:
    - `direction`: `"row"` (default) or `"column"`.
    - `justify_content`: How to align children along the main axis (e.g., `"center"`, `"space-between"`).
    - `align_items`: How to align children along the cross axis (e.g., `"center"`, `"stretch"`).
    - `gap`: Space between children.

```python
web.ui.Flex(
    direction="row",
    justify_content="space-around",
    children=[
        # ...
    ]
)
``` 