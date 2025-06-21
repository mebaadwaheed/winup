# winup/ui/textarea.py
from PySide6.QtWidgets import QTextEdit
from ... import style

class Textarea(QTextEdit):
    def __init__(self, placeholder: str = "", text: str = "", parent=None, props: dict = None, **kwargs):
        super().__init__(parent)

        if props is None:
            props = {}
        props.update(kwargs)

        if text:
            self.setPlainText(text)
        if placeholder:
            self.setPlaceholderText(placeholder)

        # Apply the rest of the properties as styles
        if props:
            style.apply_props(self, props)
