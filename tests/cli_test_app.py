"""
Simple test app for demonstrating CLI platform selection.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, component
from winup.core.platform import get_current_platform

@component(web=True, desktop=True)
def App():
    """Cross-platform test app."""
    current_platform = get_current_platform()
    
    return ui.Column(
        children=[
            ui.Label(f"🚀 WinUp CLI Test App", 
                    props={"font-weight": "bold", "font-size": "24px"}),
            ui.Label(f"Running on: {current_platform}", 
                    props={"font-size": "18px", "margin-top": "10px"}),
            ui.Label("This app was launched using the WinUp CLI!", 
                    props={"margin-top": "20px"}),
            ui.Button("Click me!", 
                     on_click=lambda: print(f"Button clicked on {current_platform}!")),
        ],
        props={"padding": "30px", "spacing": 15, "alignment": "AlignCenter"}
    )

if __name__ == "__main__":
    # This can now run without explicit platform setting
    winup.run("tests.cli_test_app:App", title="CLI Test App", width=500, height=300)
