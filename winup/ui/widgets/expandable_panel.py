from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
    Qt,
    Signal,
    QTimer,
)
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QSizePolicy
from winup import style


class ExpandablePanel(QWidget):
    """
    A collapsible panel widget. Contains a header button to toggle the visibility
    of a content area. The expansion and collapse are animated.
    """

    animationFinished = Signal()

    def __init__(
        self,
        title: str = "Expandable Panel",
        parent: QWidget = None,
        children: list = None,
        expanded: bool = False,
        animation_duration: int = 300,
        header_props: dict = None,
        content_props: dict = None,
        expand_icon: str = "▼",
        collapse_icon: str = "►",
    ):
        super().__init__(parent)
        self.is_expanded = expanded
        self._animation_duration = animation_duration
        self._title = title
        self._expand_icon = expand_icon
        self._collapse_icon = collapse_icon
        self._easing_curve = QEasingCurve.Type.InOutQuad

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Header Button
        self.toggle_button = QPushButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(expanded)
        self.toggle_button.setText(f"{self._title} {self._expand_icon if self.is_expanded else self._collapse_icon}")

        # Apply styles
        default_header_props = {"text-align": "left", "padding": "8px", "border": "none"}
        if header_props:
            default_header_props.update(header_props)
        style.styler.apply_props(self.toggle_button, default_header_props)
        
        self.main_layout.addWidget(self.toggle_button)

        # Animated container
        self.content_area = QFrame()
        self.content_area.setContentsMargins(0, 0, 0, 0)
        style.styler.apply_props(self.content_area, content_props)
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)
        self.content_area.setProperty("class", "expandable-panel-content")

        # Layout for the animated container
        content_area_layout = QVBoxLayout(self.content_area)
        content_area_layout.setContentsMargins(0, 0, 0, 0)

        # Inner widget that holds the actual content. This widget's size hint is reliable.
        self._content_widget = QWidget()
        self._content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        content_area_layout.addWidget(self._content_widget)
        content_layout = QVBoxLayout(self._content_widget)
        content_layout.setContentsMargins(10, 0, 10, 10)

        # Add children to the inner content widget
        if children:
            for child in children:
                content_layout.addWidget(child)
        
        self.content_area.setMaximumHeight(0) # Start collapsed
        self.main_layout.addWidget(self.content_area)

        # If starting expanded, schedule a resize after the event loop has processed layouts
        if self.is_expanded:
            print(f"[DEBUG] ExpandablePanel '{self._title}': Starting expanded. Scheduling toggle.")
            QTimer.singleShot(0, lambda: self.toggle(True))

        # Animation setup
        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.animation.finished.connect(self._on_animation_finished)

        # Connections
        self.toggle_button.toggled.connect(self.toggle)

    def _on_animation_finished(self):
        """Called when the animation finishes."""
        # If we expanded, allow the content to resize freely.
        if self.is_expanded:
            self.content_area.setMaximumHeight(16777215)  # Set to a large value (essentially no limit)
        self.animationFinished.emit()

    def setContent(self, widget: QWidget):
        """Sets the widget to be displayed in the content area."""
        layout = self._content_widget.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        layout.addWidget(widget)
        self._update_height()

    def add_child(self, widget: QWidget):
        """Adds a widget to the content area."""
        self._content_widget.layout().addWidget(widget)
        self._update_height()

    def _update_height(self):
        """Recalculates and sets the height of the content area if it's expanded."""
        if self.is_expanded:
            self.content_area.setMaximumHeight(self._content_widget.sizeHint().height())

    def toggle(self, checked: bool):
        """Toggles the panel's expanded/collapsed state."""
        self.is_expanded = checked
        
        icon = self._expand_icon if self.is_expanded else self._collapse_icon
        self.toggle_button.setText(f"{self._title} {icon}")

        start_height = self.content_area.height()
        end_height = self._content_widget.sizeHint().height() if self.is_expanded else 0

        self.animation.setDuration(self._animation_duration)
        self.animation.setEasingCurve(self._easing_curve)
        self.animation.setStartValue(start_height)
        self.animation.setEndValue(end_height)
        self.animation.start()

    def set_animation_duration(self, msecs: int):
        self._animation_duration = msecs

    def set_easing_curve(self, curve: QEasingCurve.Type):
        self._easing_curve = curve

    def expand(self):
        """Expands the panel."""
        self.toggle_button.setChecked(True)

    def collapse(self):
        """Collapses the panel."""
        self.toggle_button.setChecked(False) 