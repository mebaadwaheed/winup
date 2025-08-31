from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

class Dock(QWidget):
    """
    A widget that can be docked into the main window or floated.
    It serves as a container for other widgets.
    """
    def __init__(self, children: list = None, props: dict = None):
        super().__init__()
        self._dock_widget = QDockWidget()
        self._main_window = None

        # The Dock widget itself is a simple container in the layout
        # It manages the real QDockWidget, which will be added to the MainWindow
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # The content of the Dock is held in a separate widget
        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._dock_widget.setWidget(self._content_widget)

        if children:
            for child in children:
                self.add_child(child)
        
        if props:
            self.apply_props(props)
        
        # Store props for web conversion
        self.props = props

    def add_child(self, child: QWidget):
        """Adds a child to the dock's content area."""
        self._content_layout.addWidget(child)

    def apply_props(self, props: dict):
        """Apply properties to the QDockWidget."""
        title = props.get("title")
        if title:
            self._dock_widget.setWindowTitle(str(title))

        area = props.get("area")
        if area:
            self.setProperty("area", area)

        allowed_areas = props.get("allowed_areas")
        if allowed_areas:
            self.setProperty("allowed_areas", allowed_areas)

    def showEvent(self, event):
        """
        When the widget is shown, find the main window and add the QDockWidget to it.
        """
        super().showEvent(event)
        if self.window() and hasattr(self.window(), 'addDockWidget'):
            self._main_window = self.window()
            
            # Default to left dock area if not specified
            area = self.property("area") or Qt.DockWidgetArea.LeftDockWidgetArea
            
            self._main_window.addDockWidget(area, self._dock_widget)
            self._dock_widget.show()

    def setProperty(self, name, value):
        """Set properties for docking behavior."""
        if name == "area":
            area_map = {
                "left": Qt.DockWidgetArea.LeftDockWidgetArea,
                "right": Qt.DockWidgetArea.RightDockWidgetArea,
                "top": Qt.DockWidgetArea.TopDockWidgetArea,
                "bottom": Qt.DockWidgetArea.BottomDockWidgetArea,
            }
            qt_area = area_map.get(value, Qt.DockWidgetArea.AllDockWidgetAreas)
            if self._main_window:
                self._main_window.addDockWidget(qt_area, self._dock_widget)
            else:
                super().setProperty(name, qt_area)
        elif name == "allowed_areas":
            allowed = Qt.DockWidgetArea.NoDockWidgetArea
            area_map = {
                "left": Qt.DockWidgetArea.LeftDockWidgetArea,
                "right": Qt.DockWidgetArea.RightDockWidgetArea,
                "top": Qt.DockWidgetArea.TopDockWidgetArea,
                "bottom": Qt.DockWidgetArea.BottomDockWidgetArea,
                "all": Qt.DockWidgetArea.AllDockWidgetAreas
            }
            for area_str in value:
                allowed |= area_map.get(area_str, Qt.DockWidgetArea.NoDockWidgetArea)
            self._dock_widget.setAllowedAreas(allowed)
        else:
            super().setProperty(name, value)