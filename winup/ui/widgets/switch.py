from PySide6.QtWidgets import QCheckBox
from ... import style
from typing import Callable, Optional

class Switch(QCheckBox):
    """A checkbox styled to look like a modern toggle switch."""
    def __init__(self, text: str = "", is_checked: bool = False, on_toggle: Optional[Callable] = None, props: Optional[dict] = None, **kwargs):
        super().__init__(text, **kwargs)
        self.setChecked(is_checked)
        if on_toggle:
            self.toggled.connect(on_toggle)
        
        # Apply theme colors
        theme = style.styler.themes._active_theme
        text_color = theme.get("text-color", "#000000")

        # This custom stylesheet provides the switch-like appearance
        self.setStyleSheet(f"""
            QCheckBox {{
                color: {text_color};
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 40px;
                height: 20px;
                border-radius: 10px;
                background-color: #A0A0A0; /* Default disabled color */
            }}
            QCheckBox::indicator:unchecked {{
                background-color: #E0E0E0;
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme.get("primary-color", "#0078D4")};
            }}
            QCheckBox::handle {{
                width: 16px;
                height: 16px;
                border-radius: 8px;
                background-color: white;
                margin: 2px;
            }}
            QCheckBox::handle:unchecked {{
                margin-left: 2px;
            }}
            QCheckBox::handle:checked {{
                margin-left: 22px;
            }}
        """)
        if props:
            style.apply_props(self, props)
