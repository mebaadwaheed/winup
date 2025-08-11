import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui

@winup.component
def App():
    return ui.Column(children=[
        ui.Label("Hello, Tailwind CSS with WinUp!", props={"tailwind" : "text-black font-bold text-xl"}),
        ui.Button("Click Me", props={"tailwind": "bg-blue-500 text-white p-2"}),
    ])

if __name__ == "__main__":
    winup.run(main_component_path="test_tailwind_styling:App", title="Tailwind Styling Example")