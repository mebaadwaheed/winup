from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt
from ... import style

class Slider(QSlider):
    """A more intuitive slider widget that allows for advanced styling."""

    def __init__(self, min: int = 0, max: int = 100, step: int = 1, value: int = 0, 
                 on_change: callable = None, horizontal: bool = True, 
                 track_color: str = None, thumb_style: dict = None, props: dict = None, parent=None):
        
        orientation = Qt.Orientation.Horizontal if horizontal else Qt.Orientation.Vertical
        super().__init__(orientation, parent)
        
        self.setRange(min, max)
        self.setSingleStep(step)
        self.setValue(value)
        
        if on_change:
            self.valueChanged.connect(on_change)
            
        if props:
            style.styler.apply_props(self, props)
            
        self.apply_styles(track_color, thumb_style)

    def apply_styles(self, track_color: str, thumb_style: dict):
        """Applies custom styling to the slider's track and thumb."""
        stylesheet = ""
        
        # Style for the groove (the track)
        if track_color:
            stylesheet += f"""
                QSlider::groove:horizontal {{
                    background: {track_color};
                    height: 8px;
                    border-radius: 4px;
                }}
            """
        
        # Style for the handle (the thumb)
        if thumb_style:
            # Basic thumb style
            stylesheet += """
                QSlider::handle:horizontal {
                    background: #fff;
                    border: 1px solid #ccc;
                    width: 18px;
                    height: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                }
            """
            # Apply user-defined thumb styles, converting from Python dict to QSS
            thumb_qss = "; ".join([f"{key.replace('_', '-')}: {value}" for key, value in thumb_style.items()])
            stylesheet += f"QSlider::handle:horizontal {{ {thumb_qss}; }}"
            
        if stylesheet:
            self.setStyleSheet(stylesheet)
            
    def get_value(self) -> int:
        return self.value()
        
    def set_value(self, value: int):
        self.setValue(value) 