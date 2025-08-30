from PySide6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout
from PySide6.QtCore import Qt
from winup.core.component import Component

# List Component

class List(Component):
    def __init__(
        self,
        items: list[str],
        selected_index: int = None,
        props: dict = None,
        on_select: callable = None,
        multi_select: bool = False,
        ordered: bool = False,
        disabled: bool = False,
        height: int = None,
        width: int = None,
        style: dict = None,
        id: str = None,
        className: str = None,
    ):
        super().__init__(id=id, className=className, style=style)
        self.items = items
        self.selected_index = selected_index
        self.on_select = on_select
        self.multi_select = multi_select
        self.ordered = ordered
        self.disabled = disabled
        self.height = height
        self.width = width

        # Layout and render the component
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.layout().addWidget(self.render())

    def render(self):
        widget = QListWidget()
        widget.setDisabled(self.disabled)

        if self.multi_select:
            widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        else:
            widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        for i, item_text in enumerate(self.items):
            display_text = f"{i + 1}. {item_text}" if self.ordered else item_text
            item = QListWidgetItem(display_text)
            widget.addItem(item)

        if self.selected_index is not None and 0 <= self.selected_index < len(self.items):
            widget.setCurrentRow(self.selected_index)

        widget.itemSelectionChanged.connect(self.on_selection_changed)

        if self.width:
            widget.setFixedWidth(self.width)
        if self.height:
            widget.setFixedHeight(self.height)
            
        self.widget = widget
        return widget

    def on_selection_changed(self):
        if self.on_select:
            if self.multi_select:
                selected_items = [item.text() for item in self.widget.selectedItems()]
                self.on_select(selected_items)
            else:
                selected_item = self.widget.currentItem().text() if self.widget.currentItem() else None
                self.on_select(selected_item)