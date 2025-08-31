from PySide6.QtWidgets import QComboBox
from ... import style
from typing import List, Callable, Optional

class ComboBox(QComboBox):
    def __init__(self, items: List[str], on_change: Optional[Callable] = None, props: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.addItems(items)
        if props:
            style.apply_props(self, props)
        if on_change:
            self.currentTextChanged.connect(on_change)
        
        # Store props for web conversion
        self.props = props