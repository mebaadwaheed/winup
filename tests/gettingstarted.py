import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# hello_world.py
import winup
from winup import ui

# The @component decorator is optional for the main component, but good practice.
@winup.component
def App():
    """This is our main application component."""
    return ui.Column(
        props={
            "alignment": "AlignCenter", 
            "spacing": 20
        },
        children=[
            ui.Label("👋 Hello, WinUp!", props={"font-size": "24px"}),
            ui.Button("Click Me!", on_click=lambda: print("Button clicked!"))
        ]
    )

if __name__ == "__main__":
    winup.run(main_component_path="gettingstarted:App", title="My First WinUp App")