import os
import winup
from winup import ui, state, component

current_directory = state.create("current_directory", os.getcwd() + os.path.sep)
expanded_nodes = state.create("expanded_nodes", set())
selected_tree_node = state.create("selected_tree_node", "")

@component
def TreeViewPanel():
    def handle_tree_select(node_key):
        selected_tree_node.set(node_key)
        current_directory.set(node_key.replace(f"{os.path.sep}.", os.path.sep))

    def handle_tree_expand(node_key, is_expanded):
        current_expanded = expanded_nodes.get()
        if is_expanded:
            current_expanded.add(node_key)
        else:
            current_expanded.discard(node_key)
        expanded_nodes.set(current_expanded)

    cur_dir = current_directory.get()
    dir_parts = [f"{x}{os.path.sep}" for x in cur_dir.rstrip(os.path.sep).split(os.path.sep)]
    dir_tree = {}
    leaf = dir_tree
    expanded = []
    for i, d in enumerate(dir_parts):
        leaf[d] = {}
        expanded.append(d)
        leaf = leaf[d]

        node_set = expanded_nodes.get()
        new_node = ".".join(expanded)
        node_set.add(new_node)
        expanded_nodes.set(node_set)
        if i == len(dir_parts) - 1:
            selected_tree_node.set(new_node)

    leaf_contents = sorted(os.listdir(cur_dir))
    leaf_contents = [x for x in leaf_contents if x[0] != '.'] # Get rid of invisible directories
    for lc in leaf_contents:
        if os.path.isdir(cur_dir + lc):
            leaf[lc + "/"] = {}

    return ui.Row(
        children=[
            ui.Column(
                children=[
                    ui.Label(
                        "Directory Explorer"
                    ),
                    ui.TreeView(
                        data=dir_tree,
                        on_select=handle_tree_select,
                        on_expand=handle_tree_expand,
                        selected_node=selected_tree_node.get(),
                        expanded_nodes=expanded_nodes.get(),
                        width=400,
                        height = 500
                    ),
                ]
            ),
        ]
    )
