from PySide6.QtWidgets import QStackedWidget
from ... import style

class Deck(QStackedWidget):
    """
    A widget that stacks its children on top of each other, showing only one at a time.
    It's ideal for creating multi-page applications.
    """
    def __init__(self, children: list = None, props: dict = None, **kwargs):
        super().__init__(**kwargs)
        
        if props:
            style.apply_props(self, props)
        
        if children:
            for child in children:
                self.addWidget(child) 
        
        # Store props for web conversion
        self.props = props