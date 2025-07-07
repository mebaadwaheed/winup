# winup/core/window.py

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from ..shell import MenuBar, ToolBar, StatusBar
from typing import Optional

class Window(QMainWindow):
    """
    Represents a top-level application window that can hold a WinUp component.
    """
    def __init__(self, component: QWidget, title="WinUp", width=800, height=600, icon_path: Optional[str] = None, menu_bar: Optional[MenuBar] = None, tool_bar: Optional[ToolBar] = None, status_bar: Optional[StatusBar] = None):
        """
        Creates and shows a new window.

        Args:
            component (QWidget): The root WinUp component/widget to display in the window.
            title (str): The window title.
            width (int): The initial width of the window.
            height (int): The initial height of the window.
            icon_path (str, optional): Path to the window icon.
            menu_bar (MenuBar, optional): The menu bar for the window.
            tool_bar (ToolBar, optional): The tool bar for the window.
            status_bar (StatusBar, optional): The status bar for the window.
        """
        # Ensure a QApplication instance exists.
        _WinUpApp.get_instance()
        super().__init__()

        self.setWindowTitle(title)
        self.resize(width, height)
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        self.setCentralWidget(component)
        if menu_bar:
            self.setMenuBar(menu_bar)
        if tool_bar:
            self.addToolBar(tool_bar)
        if status_bar:
            self.setStatusBar(status_bar)
        self.show()

        # Register the window with the global app manager
        _winup_app.register_window(self)

class _WinUpApp:
    """Internal singleton class to manage the QApplication and windows."""
    _instance = None

    def __init__(self):
        app = QApplication.instance()
        if not isinstance(app, QApplication):
             # If no QApplication, create one. This also handles the None case.
            app = QApplication(sys.argv)
        
        self.app: QApplication = app
            
        self.windows = [] # Keep track of all open windows
        self._main_window: Optional[Window] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = _WinUpApp()
        return cls._instance

    def create_main_window(self, component: QWidget, title, width, height, icon, **shell_kwargs):
        """Creates the first, primary window for the application."""
        if self._main_window:
            raise RuntimeError("Main window has already been created.")
            
        self._main_window = Window(component, title, width, height, icon, **shell_kwargs)
        return self._main_window

    def register_window(self, window: QMainWindow):
        """Adds a window to the list of tracked windows."""
        if window not in self.windows:
            self.windows.append(window)

    def run(self):
        """Starts the Qt application event loop."""
        sys.exit(self.app.exec())

# Global instance of the application manager
_winup_app = _WinUpApp.get_instance()
