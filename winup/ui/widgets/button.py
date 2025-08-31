from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import QSize, Qt
from ... import style

class Button(QPushButton):
    def __init__(self, text: str = "Button", props: dict = None, on_click: callable = None, on_click_enabled: bool = True, **kwargs):
        super().__init__(text, **kwargs)
        
        if on_click and on_click_enabled:
            self.clicked.connect(on_click)

        # Store props for web conversion
        self.props = props or {}
        
        if props:
            style.apply_props(self, props)

    def set_text(self, text: str):
        self.setText(text)

    def on_click(self, func: callable):
        """
        Sets the function to be called when the button is clicked.
        This replaces any previously set click handler.
        """
        # Disconnect all existing handlers from the clicked signal
        try:
            self.clicked.disconnect()
        except RuntimeError:
            # This is expected if no signals were connected yet.
            pass
        self.clicked.connect(func)
        return self

    def set_icon(self, icon_path: str, size: int = 16, color: str = None):
        icon = QIcon(icon_path)
        if color:
            pixmap = icon.pixmap(QSize(size, size))
            mask = pixmap.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
            pixmap.fill(QColor(color))
            pixmap.setMask(mask)
            icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setIconSize(QSize(size, size))
        return self

    def _lighten_color(self, hex_color, factor=1.2):
        """Lighten a hex color for hover effect"""
        c = QColor(hex_color)
        c = c.lighter(int(factor * 100))
        return c.name()
