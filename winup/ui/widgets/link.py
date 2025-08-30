from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt
import webbrowser
from ... import style

class Link(QLabel):
    def __init__(self, text: str, url: str, tabs: int = 1, props: dict = None, parent=None):
        super().__init__(text, parent)
        self.url = url
        self.tabs = tabs
        self.setText(f'<a href="{url}">{text}</a>')
        
        if props:
            style.styler.apply_props(self, props)
        self.setStyleSheet("""
            QLabel {
                color: #007BFF;
                text-decoration: none;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)

    def mousePressEvent(self, event):
        for _ in range(self.tabs):
            webbrowser.open(self.url)
        super().mousePressEvent(event)
