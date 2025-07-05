import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import winup
from winup import ui, style

@winup.component
def App():
    #style.styler.themes.set_theme("dark")
    return ui.Column(children = [
        ui.Row(children = [
            ui.Label(text="Label!"),
            ui.Switch(text = "Switch me!", on_toggle = lambda switch: print("Switched!") if switch else print("Unswitched!")),
            ui.Switch(text = "Switch me!", on_toggle = lambda switch: print("Switched!") if switch else print("Unswitched!"), props={"color": "black"}),
        ])
    ])

if __name__ == "__main__":
    winup.run(
        main_component_path="switch:App",
        title="My Hot-Reloaded App",
        dev=True
    )