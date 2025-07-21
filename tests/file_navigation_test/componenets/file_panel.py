import os
from winup import ui, component, state

current_directory = state.create("current_directory")
dir_items = state.create("dir_items", [])
selected_files = state.create("selected_files", [])

@component
def FilePanel():
    cur_dir = state.get("current_directory")
    dir_items = [x for x in os.listdir(cur_dir) if x[0] != '.'] # ingnore invisible files
    dir_items = sorted([x for x in dir_items if os.path.isfile(cur_dir + x)]) # Throw out directories

    def on_file_select(items):
        selected_files.set(items)

    return ui.Column(
        children=[
            ui.Label(
                f"Current Directory:\n{current_directory.get().rstrip(os.path.sep).split(os.path.sep)[-1]}"
                ),
            ui.Label("Files"),
            ui.List(
                items=dir_items,
                multi_select=True,
                on_select=lambda item: on_file_select(item),
                width=250,
                height=500
            ),
        ]
    )
