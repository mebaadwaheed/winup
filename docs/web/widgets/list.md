# BulletedList

The `BulletedList` component renders a list of items. By default, it creates an unordered list (`<ul>`), but it can also create an ordered list (`<ol>`). Each direct child of the `BulletedList` will be automatically wrapped in a list item (`<li>`) tag.

## Usage

```python
from winup import web

@web.component
def ToDoList():
    return web.ui.Column(children=[
        web.ui.Label("Unordered List:", tag="h3"),
        web.ui.BulletedList(
            children=[
                web.ui.Label("First item"),
                web.ui.Label("Second item"),
                web.ui.Button("A button can be a list item too!")
            ]
        ),
        
        web.ui.Label("Ordered List:", tag="h3", style={'margin_top': '1rem'}),
        web.ui.BulletedList(
            tag="ol", # Use the 'tag' prop to create an ordered list
            children=[
                web.ui.Label("Step 1"),
                web.ui.Label("Step 2"),
                web.ui.Label("Step 3"),
            ]
        )
    ])
```

## Arguments
- `children` (list): A list of child components to render as items in the list.
- `tag` (str, optional): The type of list to render. Can be `"ul"` (default) or `"ol"`.
- `props` (dict, optional): A dictionary of additional HTML attributes to apply to the `<ul>` or `<ol>` element.
- `**kwargs`: Keyword arguments are also treated as HTML attributes. 