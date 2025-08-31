from PySide6.QtWidgets import QCheckBox
from ... import style

class Checkbox(QCheckBox):
    def __init__(self, text: str = "Checkbox", props: dict = None, on_toggle: callable = None, **kwargs):
        super().__init__(text, **kwargs)
        if on_toggle:
            self.toggled.connect(on_toggle)
        if props:
            style.apply_props(self, props)

        # Store props for web conversion
        self.props = props

    def set_text(self, text: str):
        self.setText(text)

    def on_toggle(self, func: callable):
        """
        Sets the function to be called when the checkbox is toggled.
        This replaces any previously set toggle handler.
        """
        try:
            self.toggled.disconnect()
        except RuntimeError:
            pass
        self.toggled.connect(func)
        return self

    def is_checked(self):
        return self.isChecked()

    def set_checked(self, checked: bool):
        self.setChecked(checked)
        return self 