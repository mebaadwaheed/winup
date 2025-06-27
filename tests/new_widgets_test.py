import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import winup
from winup import ui, state, style

def NewWidgetsTestApp():

    label_color = state.create("label_color", "#000000")
    selected_list_item = state.create("selected_list_item", "None")
    selected_tree_node = state.create("selected_tree_node", "root.parent1.child1")
    expanded_nodes = state.create("expanded_nodes", {"root", "root.parent1"})

    def handle_color_change(new_color):
        label_color.set(new_color)

    def handle_list_select(selected_item):
        selected_list_item.set(str(selected_item))

    def handle_tree_select(node_key):
        selected_tree_node.set(node_key)

    def handle_tree_expand(node_key, is_expanded):
        current_expanded = expanded_nodes.get()
        if is_expanded:
            current_expanded.add(node_key)
        else:
            current_expanded.discard(node_key)
        expanded_nodes.set(current_expanded)


    tree_data = {
        "root": {
            "parent1": {
                "child1": {},
                "child2": {}
            },
            "parent2": {
                "child3": {},
                "child4": {
                    "grandchild1": {}
                }
            }
        }
    }

    color_label = ui.Label()
    label_color.bind_to(color_label, 'style', lambda c: {"color": c, "font-size": "24px", "font-weight": "bold"})
    label_color.bind_to(color_label, 'text', lambda c: f"Selected Color: {c}")


    list_selection_label = ui.Label()
    selected_list_item.bind_to(list_selection_label, 'text', lambda i: f"Selected: {i}")

    tree_selection_label = ui.Label()
    selected_tree_node.bind_to(tree_selection_label, 'text', lambda n: f"Selected Node: {n}")


    def set_theme(theme_name):
        style.themes.set_theme(theme_name)

    return ui.Column(props={"spacing": 10, "margin": "15px"}, children=[
        ui.Row(props={"spacing": 10}, children=[
            ui.Button("Light Theme", on_click=lambda: set_theme("light")),
            ui.Button("Dark Theme", on_click=lambda: set_theme("dark")),
        ]),
        color_label,

        ui.ColorPicker(
            selected_color=label_color.get(),
            on_change=handle_color_change,
            preset_colors=["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]
        ),

        ui.Row(props={"spacing": 20, "margin-top": "20px"}, children=[
            ui.Column(props={"spacing": 5}, children=[
                ui.Label("Ordered List (Single Select)", props={"font-weight": "bold"}),
                ui.List(
                    items=["Apple", "Banana", "Cherry", "Date"],
                    on_select=handle_list_select,
                    ordered=True,
                    width=200,
                    height=150
                ),
                list_selection_label,
            ]),

            ui.Column(props={"spacing": 5}, children=[
                ui.Label("File Explorer (Tree View)", props={"font-weight": "bold"}),
                ui.TreeView(
                    data=tree_data,
                    on_select=handle_tree_select,
                    on_expand=handle_tree_expand,
                    selected_node=selected_tree_node.get(),
                    expanded_nodes=expanded_nodes.get(),
                    width=300,
                    height=200,
                ),
                tree_selection_label,
            ]),
        ]),
    ])


if __name__ == "__main__":
    winup.run(
        main_component_path="new_widgets_test:NewWidgetsTestApp",
        title="New Widgets Test",
        width=600,
        height=400,
        dev=True,
    )
