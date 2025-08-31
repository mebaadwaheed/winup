from PySide6.QtWidgets import QLabel
from ... import style

class Label(QLabel):
    def __init__(self, text: str = "", props: dict = None, bold: bool = False, font_size: int = None, **kwargs):
        super().__init__(text, **kwargs)
        
        # Ensure props is a dictionary
        if props is None:
            props = {}
            
        # Add bold styling if requested
        if bold:
            props['font-weight'] = 'bold'

        if font_size:
            props['font-size'] = f"{font_size}px"
            
        # Store props for web conversion
        self.props = props
        
        if props:
            style.apply_props(self, props)

    def set_text(self, text: str):
        """A more Pythonic alias for setText()."""
        self.setText(text)
