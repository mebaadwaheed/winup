import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
import winup.ui as ui

@winup.component
def TailwindTest():
    return ui.Column(
        children=[
            ui.Label("Tailwind Test", props={'tailwind': ''}),
            ui.Button("Click Me", props={'tailwind': 'bg-blue-500 text-white p-4'}),
        ]
    )

if __name__ == '__main__':
    winup.run(main_component_path="new_tailwind:TailwindTest", title="Tailwind Test", dev=True)
