from PySide6.QtWidgets import QFrame, QWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout
from ..layout_managers import VBox, HBox
from ... import style

class Frame(QFrame):
    def __init__(self, children: list = None, props: dict = None, parent: QWidget = None, **kwargs):
        # All custom keyword arguments will be treated as style properties.
        # This is a more robust way to handle styling.
        if props is None:
            props = {}
        props.update(kwargs)

        # Now that all kwargs are in props, call the parent constructor with the parent argument.
        super().__init__(parent)
        
        # Intercept and handle lifecycle hooks from the combined props
        on_mount = props.pop('on_mount', None)
        on_unmount = props.pop('on_unmount', None)
        self._on_mount_handler = on_mount
        self._on_unmount_handler = on_unmount

        self._layout = None

        # Set object ID from props if it exists
        if 'id' in props:
            self.setObjectName(props.pop('id'))

        # Process layout property first if it exists in props
        if "layout" in props:
            layout_type = props.pop("layout")
            self.set_layout(layout_type)

        # Apply the rest of the properties as styles
        if props:
            style.apply_props(self, props)
        
        # Now add children
        if children:
            if self.layout() is None:
                self.set_layout(VBox())
            self.add_children(children)

    def set_layout(self, layout):
        # Allow setting layout with string shortcuts "vertical" or "horizontal"
        if isinstance(layout, str):
            if layout.lower() == "vertical":
                layout_obj = VBox()
            elif layout.lower() == "horizontal":
                layout_obj = HBox()
            else:
                raise ValueError(f"Unknown layout string: '{layout}'. Use 'vertical' or 'horizontal'.")
        else:
            layout_obj = layout

        # Clear any existing layout and its widgets before setting a new one.
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        
        self.setLayout(layout_obj)

    def add_child(self, child: QWidget, stretch: int = 0):
        if self.layout() is None:
            raise RuntimeError("Cannot add child to a Frame without a layout. Call set_layout() first.")
        
        if not hasattr(self.layout(), 'addWidget'):
            raise TypeError("The layout for this Frame does not support adding widgets.")

        # Check if the layout supports stretch (i.e., it's a box layout)
        if isinstance(self.layout(), QBoxLayout):
            self.layout().addWidget(child, stretch=stretch)
        else:
            # For other layouts (like Stacked or Grid), just add the widget without stretch.
            self.layout().addWidget(child)

    def showEvent(self, event):
        """QWidget override to trigger the on_mount event."""
        super().showEvent(event)
        if hasattr(self, '_on_mount_handler') and self._on_mount_handler:
            self._on_mount_handler()
            # To prevent it from being called multiple times
            self._on_mount_handler = None

    def closeEvent(self, event):
        """QWidget override to trigger the on_unmount event."""
        if hasattr(self, '_on_unmount_handler') and self._on_unmount_handler:
            self._on_unmount_handler()
        super().closeEvent(event)

    def add_children(self, children: list):
        if not children:
            raise ValueError("Cannot add children to a Frame without a list of children.")
        
        if self.layout() is None:
            raise RuntimeError("Cannot add children to a Frame without a layout. Call set_layout() first.")
        
        if not hasattr(self.layout(), 'addWidget'):
            raise TypeError("The layout for this Frame does not support adding widgets.")

        # Check if the layout supports stretch (i.e., it's a box layout)
        if isinstance(self.layout(), QBoxLayout):
            for child in children:
                self.add_child(child)
        else:
            # For other layouts (like Stacked or Grid), just add the widgets without stretch.
            for child in children:
                self.layout().addWidget(child)

    def place_child(self, child: QWidget, x: int, y: int, width: int = None, height: int = None):
        """
        Places a child widget at absolute coordinates within the Frame.
        This method ONLY works if the Frame has NO layout manager set.
        """
        if self.layout() is not None:
            raise RuntimeError(
                "Cannot use .place_child() on a Frame that has a layout manager. "
                "For absolute positioning, create a Frame with no layout."
            )
        
        child.setParent(self)
        
        # If width/height are not provided, use the child's size hint
        size_hint = child.sizeHint()
        effective_width = width if width is not None else size_hint.width()
        effective_height = height if height is not None else size_hint.height()

        child.setGeometry(x, y, effective_width, effective_height)
        child.show()