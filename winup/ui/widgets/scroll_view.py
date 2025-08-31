from PySide6.QtWidgets import QScrollArea, QWidget
from PySide6.QtCore import Qt
from ... import style
from ..layouts import VBox

class ScrollView(QScrollArea):
    """
    A scrollable area that can contain a single child widget.
    Typically used with a Column or Row to display a growing list of items.
    """
    def __init__(self, child: QWidget, props: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.setWidget(child)
        self.content_widget = child

        if props:
            style.apply_props(self, props)
        
        # Store props for web conversion
        self.props = props

    def scroll_to_bottom(self):
        """Automatically scrolls to the bottom of the content."""
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def add_child(self, widget: QWidget):
        """
        Adds a child to the ScrollView's content widget.
        Note: The content widget must have an `add_child` method (e.g., Frame, Column, Row).
        """
        if hasattr(self.content_widget, 'add_child'):
            self.content_widget.add_child(widget)
        else:
            raise TypeError("The content widget of this ScrollView does not support adding children.")

    def set_widget(self, widget: QWidget):
        self.setWidget(widget)
        self.content_widget = widget 