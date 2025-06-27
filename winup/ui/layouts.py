from .widgets.frame import Frame
from .layout_managers import VBox, HBox, StackBox, GridBox

class Column(Frame):
    """A Frame that arranges child widgets vertically using a VBox layout."""
    def __init__(self, children: list = None, props: dict = None, parent=None, **kwargs):
        # Separate frame props from layout props
        frame_props = props.copy() if props else {}
        layout_props = {
            "alignment": frame_props.pop("alignment", None),
            "spacing": frame_props.pop("spacing", None),
            "margin": frame_props.pop("margin", None)
        }
        layout_props = {k: v for k, v in layout_props.items() if v is not None}
        
        super().__init__(props=frame_props, parent=parent, **kwargs)
        
        self.set_layout(VBox(props=layout_props))
        if children:
            for item in children:
                if isinstance(item, tuple) and len(item) == 2:
                    widget, child_props = item
                    stretch = child_props.get("stretch", 0)
                    self.add_child(widget, stretch=stretch)
                else:
                    self.add_child(item)

class Row(Frame):
    """A Frame that arranges child widgets horizontally using an HBox layout."""
    def __init__(self, children: list = None, props: dict = None, parent=None, **kwargs):
        # Separate frame props from layout props
        frame_props = props.copy() if props else {}
        layout_props = {
            "alignment": frame_props.pop("alignment", None),
            "spacing": frame_props.pop("spacing", None),
            "margin": frame_props.pop("margin", None)
        }
        layout_props = {k: v for k, v in layout_props.items() if v is not None}
        
        super().__init__(props=frame_props, parent=parent, **kwargs)

        self.set_layout(HBox(props=layout_props))
        if children:
            for item in children:
                if isinstance(item, tuple) and len(item) == 2:
                    widget, child_props = item
                    stretch = child_props.get("stretch", 0)
                    self.add_child(widget, stretch=stretch)
                else:
                    self.add_child(item)

class Stack(Frame):
    """
    A Frame that stacks child widgets on top of each other.
    Only one widget is visible at a time.
    """
    def __init__(self, children: list = None, props: dict = None, **kwargs):
        super().__init__(props=props, **kwargs)
        
        self.set_layout(StackBox())
        if children:
            for child in children:
                self.add_child(child)

    def set_current_index(self, index: int):
        """Sets the currently visible widget by its index."""
        if self.layout() and hasattr(self.layout(), 'setCurrentIndex'):
            self.layout().setCurrentIndex(index)

    def set_current_widget(self, widget):
        """Sets the currently visible widget by its instance."""
        if self.layout() and hasattr(self.layout(), 'setCurrentWidget'):
            self.layout().setCurrentWidget(widget)

class Grid(Frame):
    """
    A Frame that arranges child widgets in a grid.
    Children should be provided as a list of tuples, where each tuple is:
    (widget, row, col) or (widget, row, col, row_span, col_span)
    """
    def __init__(self, children: list = None, props: dict = None, **kwargs):
        # Separate frame props from layout props
        frame_props = props.copy() if props else {}
        layout_props = {
            "spacing": frame_props.pop("spacing", None),
            "margin": frame_props.pop("margin", None),
            "horizontal-spacing": frame_props.pop("horizontal-spacing", None),
            "vertical-spacing": frame_props.pop("vertical-spacing", None),
        }
        layout_props = {k: v for k, v in layout_props.items() if v is not None}
        
        super().__init__(props=frame_props, **kwargs)
        
        self.set_layout(GridBox(props=layout_props))
        if children:
            for item in children:
                self.add_child_at(item)

    def add_child_at(self, item: tuple):
        """Adds a child to the grid at a specific position."""
        if not self.layout() or not isinstance(self.layout(), GridBox):
            raise TypeError("The layout for this Grid is not a GridBox.")
        
        if not isinstance(item, (list, tuple)):
            raise TypeError(f"Grid children must be tuples or lists, not {type(item).__name__}")
        
        # Unpack the tuple, providing defaults for spans
        widget, row, col, row_span, col_span = (*item, 1, 1)[:5]
        
        self.layout().addWidget(widget, row, col, row_span, col_span) 