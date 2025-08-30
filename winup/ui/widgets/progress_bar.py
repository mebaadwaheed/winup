from PySide6.QtWidgets import QProgressBar
from ... import style

class ProgressBar(QProgressBar):
    """A simple progress bar widget."""

    def __init__(self, min_val: int = 0, max_val: int = 100, default_val: int = 0, props: dict = None, parent=None):
        super().__init__(parent)
        self.setRange(min_val, max_val)
        self.setValue(default_val)
        
        # Set default styling for better appearance
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                color: white;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 8px;
            }
        """)
        
        if props:
            style.styler.apply_props(self, props)
        
    def get_value(self) -> int:
        return self.value()
        
    def set_value(self, value: int):
        self.setValue(value)