from PySide6.QtWidgets import QPushButton, QColorDialog, QVBoxLayout
from PySide6.QtGui import QColor
from winup.core.component import Component
from winup.state.manager import StateManager

class ColorPicker(Component):
    def __init__(
        self,
        selected_color: str,
        on_change: callable = None,
        props: dict = None,
        enable_alpha: bool = False,
        preset_colors: list = None,
        disabled: bool = False,
        style: dict = None,
        id: str = None,
        className: str = None,
    ):
        super().__init__(id=id, className=className, style=style)
        self.selected_color = selected_color
        self.on_change = on_change
        self.enable_alpha = enable_alpha
        self.preset_colors = preset_colors
        self.disabled = disabled

        # Layout and render the component
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.layout().addWidget(self.render())

        # Store props for web conversion
        self.props = props

    def render(self):
        widget = QPushButton()
        widget.setText(f"Color: {self.selected_color}")
        widget.setStyleSheet(f"background-color: {self.selected_color}")
        widget.setDisabled(self.disabled)
        widget.clicked.connect(self.show_color_dialog)
        self.widget = widget
        return widget

    def show_color_dialog(self):
        color_dialog = QColorDialog()
        if self.enable_alpha:
            color_dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel)

        if self.preset_colors:
            for i, color in enumerate(self.preset_colors):
                color_dialog.setCustomColor(i, QColor(color))

        initial_color = QColor(self.selected_color)
        color = color_dialog.getColor(initial=initial_color)

        if color.isValid():
            new_color = color.name() if not self.enable_alpha else color.name(QColor.NameFormat.HexArgb)
            self.selected_color = new_color
            self.widget.setText(f"Color: {self.selected_color}")
            self.widget.setStyleSheet(f"background-color: {self.selected_color}")

            if self.on_change:
                self.on_change(new_color) 