"""
Layout Showcase Example - Cross-Platform Layout Demonstration

This example showcases different layout options and styling capabilities
of the unified component system across desktop and web platforms.

Usage:
    # Desktop mode
    winup run examples.layout_showcase:LayoutApp --desktop
    
    # Web mode
    winup run examples.layout_showcase:LayoutApp --web --port 8002
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, component
from winup.core.platform import get_current_platform

@component(web=True, desktop=True)
def LayoutApp():
    """Demonstrates various layout options and alignment features."""
    platform = get_current_platform()
    
    return ui.Column(
        children=[
            # Header
            ui.Label("🎨 Layout Showcase", 
                    props={"font-size": "26px", "font-weight": "bold", "color": "#2c3e50"}),
            ui.Label(f"Platform: {platform}", 
                    props={"font-size": "14px", "color": "#7f8c8d", "margin-bottom": "20px"}),
            
            # Centered content section
            ui.Column(
                children=[
                    ui.Label("Centered Column", 
                            props={"font-weight": "bold", "color": "#3498db"}),
                    ui.Label("This content is centered"),
                    ui.Button("Centered Button", 
                             props={"background-color": "#3498db", "color": "white", "padding": "8px 16px"})
                ],
                props={"alignment": "AlignCenter", "spacing": 10, "padding": "20px", 
                       "background-color": "#ecf0f1", "border-radius": "8px", "margin": "10px 0"}
            ),
            
            # Horizontal row layout
            ui.Row(
                children=[
                    ui.Column(
                        children=[
                            ui.Label("Left Column", props={"font-weight": "bold", "color": "#e74c3c"}),
                            ui.Label("Left aligned content"),
                            ui.Button("Left Button", 
                                     props={"background-color": "#e74c3c", "color": "white", "padding": "6px 12px"})
                        ],
                        props={"alignment": "AlignLeft", "spacing": 8, "padding": "15px", 
                               "background-color": "#fdf2f2", "border-radius": "6px", "flex": "1"}
                    ),
                    ui.Column(
                        children=[
                            ui.Label("Right Column", props={"font-weight": "bold", "color": "#27ae60"}),
                            ui.Label("Right aligned content"),
                            ui.Button("Right Button", 
                                     props={"background-color": "#27ae60", "color": "white", "padding": "6px 12px"})
                        ],
                        props={"alignment": "AlignRight", "spacing": 8, "padding": "15px", 
                               "background-color": "#f2fdf2", "border-radius": "6px", "flex": "1"}
                    )
                ],
                props={"spacing": 15, "margin": "10px 0"}
            ),
            
            # Grid-like layout using rows
            ui.Label("Grid Layout Simulation", 
                    props={"font-weight": "bold", "margin-top": "20px", "color": "#8e44ad"}),
            ui.Row(
                children=[
                    ui.Button("1", props={"padding": "15px", "background-color": "#9b59b6", "color": "white", "flex": "1"}),
                    ui.Button("2", props={"padding": "15px", "background-color": "#8e44ad", "color": "white", "flex": "1"}),
                    ui.Button("3", props={"padding": "15px", "background-color": "#9b59b6", "color": "white", "flex": "1"})
                ],
                props={"spacing": 5, "margin": "10px 0"}
            ),
            ui.Row(
                children=[
                    ui.Button("4", props={"padding": "15px", "background-color": "#8e44ad", "color": "white", "flex": "1"}),
                    ui.Button("5", props={"padding": "15px", "background-color": "#9b59b6", "color": "white", "flex": "1"}),
                    ui.Button("6", props={"padding": "15px", "background-color": "#8e44ad", "color": "white", "flex": "1"})
                ],
                props={"spacing": 5}
            )
        ],
        props={"padding": "30px", "spacing": 15}
    )

if __name__ == "__main__":
    winup.run("examples.layout_showcase:LayoutApp", title="Layout Showcase - WinUp", width=600, height=700)
