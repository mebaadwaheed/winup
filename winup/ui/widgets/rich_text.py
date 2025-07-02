from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QBrush
from typing import Dict, Any, Optional
from ... import style

class RichText(QTextEdit):
    def __init__(self, text: str = "", html: str = "", props: Optional[Dict[str, Any]] = None, read_only: bool = False, **kwargs):
        super().__init__(**kwargs)
        
        # Ensure props is a dictionary
        if props is None:
            props = {}
            
        # Set read-only state
        self.setReadOnly(read_only)
        
        # Set initial content
        if html:
            self.setHtml(html)
        else:
            self.setPlainText(text)
            
        if props:
            style.apply_props(self, props)
    
    def _convert_to_qcolor(self, color_str: str) -> QBrush:
        """Convert a color string to a QBrush."""
        return QBrush(QColor(color_str))
    
    def set_text(self, text: str):
        """A more Pythonic alias for setPlainText()."""
        self.setPlainText(text)
        
    def set_html(self, html: str):
        """A more Pythonic alias for setHtml()."""
        self.setHtml(html)
        
    def append_text(self, text: str, format_dict: Optional[Dict[str, Any]] = None):
        """
        Append text with optional formatting.
        
        Args:
            text: The text to append
            format_dict: Optional dictionary of text formatting properties
                e.g., {"color": "red", "bold": True, "size": 14}
                Supported colors: Any CSS color name or hex code
        """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        if format_dict:
            format = QTextCharFormat()
            
            if "color" in format_dict:
                format.setForeground(self._convert_to_qcolor(format_dict["color"]))
            if "background" in format_dict:
                format.setBackground(self._convert_to_qcolor(format_dict["background"]))
            if format_dict.get("bold", False):
                format.setFontWeight(700)  # Bold weight
            if format_dict.get("italic", False):
                format.setFontItalic(True)
            if format_dict.get("underline", False):
                format.setFontUnderline(True)
            if "size" in format_dict:
                format.setFontPointSize(format_dict["size"])
                
            cursor.insertText(text, format)
        else:
            cursor.insertText(text)
            
        self.setTextCursor(cursor)
        
    def clear(self):
        """A more Pythonic alias for clear()."""
        super().clear()
        
    def get_text(self) -> str:
        """A more Pythonic alias for toPlainText()."""
        return self.toPlainText()
        
    def get_html(self) -> str:
        """A more Pythonic alias for toHtml()."""
        return self.toHtml() 