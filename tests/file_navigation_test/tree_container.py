from winup import ui, state
import winup
import sys, os
from componenets.dir_tree_panel import TreeViewPanel
from componenets.file_panel import FilePanel

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

dir_files = state.create("dir_files")
current_directory = state.create("current_directory")

dir_label = ui.Label(text=current_directory.get()[-1])
current_directory.bind_to(
    dir_label,
    'text',
    lambda cd: f"Directory: {current_directory.get()[-1]}"
)

def App():
    file_list_container = ui.Frame(props={"id": "file_list_container", "layout": "vertical"})
    directory_tree_container = ui.Frame(props={"id": "directory_tree_container", "layout": "vertical"})

    def on_dir_change(cur_dir):
        ui.clear_layout(directory_tree_container.layout())
        ui.clear_layout(file_list_container.layout())

        directory_tree_container.add_child(TreeViewPanel())
        file_list_container.add_child(FilePanel())

    state.subscribe("current_directory", on_dir_change)

    on_dir_change(state.get("current_directory")) # Initial page load

    return ui.Row(
        children=[
            directory_tree_container,
            file_list_container,
        ]
    )

if __name__ == '__main__':
    winup.run(main_component_path="tree_container:App", title="Messing about with directory navigation")
