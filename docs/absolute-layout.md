# Advanced: Absolute Positioning with `.place_child()`

While WinUp's standard layout system (`Row`, `Column`, `Grid`) is recommended for most user interfaces, sometimes you need pixel-perfect control over the position and size of your widgets. For these advanced cases, you can use a layout-less `Frame` as a canvas and place widgets at absolute coordinates using the `.place_child()` method.

**This is an advanced feature. Only use it when standard layouts are not sufficient.** Using absolute positioning can make your UI less responsive to window resizing and changes in content.

## How it Works

The `.place_child()` method works on a `Frame` instance, but **only if that `Frame` has no layout manager**.

1.  To create a "canvas" for absolute positioning, instantiate a `Frame` **without** passing any `children` or a `layout` prop.
2.  Use the `my_frame.place_child()` method to add and position widgets inside it.

```python
from winup import ui, winup

@winup.component
def AbsoluteLayoutExample():
    # 1. Create a layout-less Frame to act as the canvas.
    #    Give it a fixed size and some style to make it visible.
    canvas = ui.Frame(props={
        "min-width": "400px",
        "min-height": "300px",
        "background-color": "#2c3e50",
        "border": "2px solid white"
    })

    # 2. Create the widgets you want to place.
    label = ui.Label(
        "I am at a precise location (50, 20).", 
        props={"color": "white"}
    )
    button = ui.Button("You can overlap me!")

    # 3. Place them on the canvas at specific x, y coordinates.
    canvas.place_child(label, x=50, y=20)
    canvas.place_child(button, x=40, y=100)

    # You can even place widgets on top of each other.
    another_label = ui.Label(
        "I'm on top!", 
        props={"background-color": "red", "padding": "5px", "color": "white"}
    )
    canvas.place_child(another_label, x=130, y=90)
    
    return canvas
```

## Method Signature

### `frame.place_child(child, x, y, width=None, height=None)`

- `child: QWidget`: The widget instance you want to place.
- `x: int`: The horizontal coordinate (in pixels) from the left edge of the `Frame`.
- `y: int`: The vertical coordinate (in pixels) from the top edge of the `Frame`.
- `width: int` (optional): If provided, the widget will be set to this width. If `None`, the widget's default preferred width (`sizeHint`) is used.
- `height: int` (optional): If provided, the widget will be set to this height. If `None`, the widget's default preferred height (`sizeHint`) is used. 