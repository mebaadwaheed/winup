"""
Hello World Example - Cross-Platform WinUp App

This example demonstrates the basic usage of the unified @component decorator
that works on both desktop and web platforms.

Usage:
    # Desktop mode
    winup run examples.hello_world:App --desktop
    
    # Web mode
    winup run examples.hello_world:App --web --web-port 8000
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, component
from winup.core.platform import get_current_platform

@component(web=True, desktop=True)
def App():
    """A simple Hello World app that works on both platforms."""
    platform = get_current_platform()
    
    return ui.Column(
        children=[
            ui.Label("👋 Hello, WinUp!", 
                    props={"font-size": "28px", "font-weight": "bold", "color": "#2c3e50"}),
            ui.Label(f"Running on {platform} platform", 
                    props={"font-size": "16px", "margin-top": "15px", "color": "#7f8c8d"}),
            ui.Label("This is a cross-platform component!", 
                    props={"margin-top": "10px"}),
            ui.Button("Say Hello!", 
                     on_click=lambda: print(f"Hello from {platform}!"),
                     props={"margin-top": "20px", "padding": "10px 20px", "background-color": "#3498db", "color": "white"})
        ],
        props={"padding": "40px", "spacing": 20, "alignment": "AlignCenter"}
    )

if __name__ == "__main__":
    winup.run("examples.hello_world:App", title="Hello World - WinUp", width=400, height=300)
