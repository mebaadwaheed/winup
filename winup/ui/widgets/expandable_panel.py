from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
    Qt,
    Signal,
)
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget, QLabel


class ExpandablePanel(QWidget):
    """
    A collapsible panel widget. Contains a header button to toggle the visibility
    of a content area. The expansion and collapse are animated.
    """

    animationFinished = Signal()

    def __init__(
        self, title: str = "Expandable Panel", parent: QWidget = None, children: list = None
    ):
        super().__init__(parent)
        self.is_expanded = False
        self._animation_duration = 300
        self._easing_curve = QEasingCurve.Type.InOutQuad

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Toggle button (header)
        self.toggle_button = QPushButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                padding: 8px;
                border: none;
                background-color: transparent;
            }
            """
        )
        self.toggle_button.setProperty("class", "expandable-panel-header")
        self.main_layout.addWidget(self.toggle_button)
        
        # Icon label (e.g., for a chevron)
        self.icon_label = QLabel("►")
        self.icon_label.setFixedWidth(20)
        self.toggle_button.setLayout(QVBoxLayout())
        self.toggle_button.layout().addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignRight)


        # Content area
        self.content_area = QFrame()
        self.content_area.setLayout(QVBoxLayout())
        self.content_area.setContentsMargins(10, 0, 10, 10)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)
        self.content_area.setProperty("class", "expandable-panel-content")
        self.main_layout.addWidget(self.content_area)

        # Add children if provided
        if children:
            for child in children:
                self.content_area.layout().addWidget(child)

        # Animation setup
        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.animation.finished.connect(self.animationFinished.emit)

        # Connections
        self.toggle_button.toggled.connect(self.toggle)

    def setContent(self, widget: QWidget):
        """Sets the widget to be displayed in the content area."""
        layout = self.content_area.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        layout.addWidget(widget)

    def add_child(self, widget: QWidget):
        """Adds a widget to the content area."""
        self.content_area.layout().addWidget(widget)

    def toggle(self, checked: bool):
        """Toggles the panel's expanded/collapsed state."""
        self.is_expanded = checked
        
        self.icon_label.setText("▼" if self.is_expanded else "►")

        # Configure the animation properties each time to ensure it has an end value.
        # The end value is the natural height of the content layout.
        end_height = self.content_area.layout().sizeHint().height()
        self.animation.setDuration(self._animation_duration)
        self.animation.setEasingCurve(self._easing_curve)
        self.animation.setStartValue(0)
        self.animation.setEndValue(end_height)

        self.animation.setDirection(
            QPropertyAnimation.Direction.Forward
            if self.is_expanded
            else QPropertyAnimation.Direction.Backward
        )
        
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