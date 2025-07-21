# TreeView Component 
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout
from winup.core.component import Component

class TreeView(Component):
    def __init__(
        self,
        data: dict,
        expanded_nodes: set = None,
        selected_node: str = None,
        on_select: callable = None,
        on_expand: callable = None,
        show_icons: bool = True, # Icon functionality not yet implemented
        height: int = None,
        width: int = None,
        style: dict = None,
        id: str = None,
        className: str = None,
    ):
        super().__init__(id=id, className=className, style=style)
        self.data = data
        self.expanded_nodes = expanded_nodes if expanded_nodes is not None else set()
        self.selected_node = selected_node
        self.on_select = on_select
        self.on_expand = on_expand
        self.show_icons = show_icons
        self.height = height
        self.width = width
        self.node_map = {}

        # Layout and render the component
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.layout().addWidget(self.render())

    def render(self):
        widget = QTreeWidget()
        self.widget = widget
        widget.setHeaderHidden(True)
        self.populate_tree(widget, self.data)

        if self.width:
            widget.setFixedWidth(self.width)
        if self.height:
            widget.setFixedHeight(self.height)
        
        widget.itemSelectionChanged.connect(self.handle_selection)
        widget.itemExpanded.connect(self.handle_expand)
        widget.itemCollapsed.connect(self.handle_collapse)

        if self.selected_node and self.selected_node in self.node_map:
            self.node_map[self.selected_node].setSelected(True)
            # Ensure the selected node is visible
            widget.scrollToItem(self.node_map[self.selected_node])

        return widget

    def populate_tree(self, parent_widget, data, parent_key=''):
        if isinstance(parent_widget, QTreeWidget):
            parent_widget.clear()
            self.node_map.clear()

        for key, value in data.items():
            # Create a unique key for each node to handle duplicate names
            unique_key = f"{parent_key}.{key}" if parent_key else key
            
            item = QTreeWidgetItem(parent_widget)
            item.setText(0, key)
            self.node_map[unique_key] = item
            
            if unique_key in self.expanded_nodes:
                item.setExpanded(True)

            if isinstance(value, dict):
                self.populate_tree(item, value, unique_key)

    def get_key_from_item(self, item_to_find):
        for key, item in self.node_map.items():
            if item == item_to_find:
                return key
        return None

    def handle_selection(self):
        if not self.on_select:
            return
        selected_items = self.widget.selectedItems()
        if selected_items:
            selected_key = self.get_key_from_item(selected_items[0])
            if selected_key:
                self.selected_node = selected_key
                self.on_select(selected_key)

    def handle_expand(self, item):
        if not self.on_expand:
            return
        key = self.get_key_from_item(item)
        if key:
            self.expanded_nodes.add(key)
            self.on_expand(key, True)

    def handle_collapse(self, item):
        if not self.on_expand:
            return
        key = self.get_key_from_item(item)
        if key:
            self.expanded_nodes.discard(key)
            self.on_expand(key, False)