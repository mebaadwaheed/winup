"""
Platform-Specific Example - Demonstrating Platform-Targeted Components

This example shows how to create components that target specific platforms
using the @component decorator's platform parameters.

Usage:
    # Desktop-only component
    winup run examples.platform_specific:DesktopOnlyApp --desktop
    
    # Web-only component  
    winup run examples.platform_specific:WebOnlyApp --web --web-port 8003
    
    # Cross-platform component
    winup run examples.platform_specific:CrossPlatformApp --desktop
    winup run examples.platform_specific:CrossPlatformApp --web --web-port 8004
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, component
from winup.core.platform import get_current_platform

@component(desktop=True, web=False)
def DesktopOnlyApp():
    """A component that only works on desktop platform."""
    return ui.Column(
        children=[
            ui.Label("🖥️ Desktop-Only App", 
                    props={"font-size": "24px", "font-weight": "bold", "color": "#2c3e50"}),
            ui.Label("This component is designed specifically for desktop", 
                    props={"margin-top": "15px"}),
            ui.Label("Features desktop-specific optimizations", 
                    props={"margin-top": "10px", "color": "#7f8c8d"}),
            ui.Button("Desktop Action", 
                     on_click=lambda: print("Desktop-specific action performed!"),
                     props={"margin-top": "20px", "padding": "10px 20px", "background-color": "#34495e", "color": "white"})
        ],
        props={"padding": "40px", "spacing": 15, "alignment": "AlignCenter"}
    )

@component(web=True, desktop=False)
def WebOnlyApp():
    """A component that only works on web platform."""
    return ui.Column(
        children=[
            ui.Label("🌐 Web-Only App", 
                    props={"font-size": "24px", "font-weight": "bold", "color": "#e67e22"}),
            ui.Label("This component is optimized for web browsers", 
                    props={"margin-top": "15px"}),
            ui.Label("Includes web-specific features and styling", 
                    props={"margin-top": "10px", "color": "#7f8c8d"}),
            ui.Button("Web Action", 
                     on_click=lambda: print("Web-specific action performed!"),
                     props={"margin-top": "20px", "padding": "10px 20px", "background-color": "#d35400", "color": "white"})
        ],
        props={"padding": "40px", "spacing": 15, "alignment": "AlignCenter"}
    )

@component(web=True, desktop=True)
def CrossPlatformApp():
    """A component that adapts to both platforms."""
    platform = get_current_platform()
    
    # Platform-specific styling
    if platform == 'web':
        primary_color = "#3498db"
        platform_emoji = "🌐"
        platform_message = "Optimized for web browsers with responsive design"
    else:
        primary_color = "#2c3e50"
        platform_emoji = "🖥️"
        platform_message = "Native desktop experience with Qt widgets"
    
    return ui.Column(
        children=[
            ui.Label(f"{platform_emoji} Cross-Platform App", 
                    props={"font-size": "24px", "font-weight": "bold", "color": primary_color}),
            ui.Label(f"Currently running on: {platform}", 
                    props={"font-size": "16px", "margin-top": "10px", "color": "#7f8c8d"}),
            ui.Label(platform_message, 
                    props={"margin-top": "15px", "text-align": "center"}),
            
            ui.Row(
                children=[
                    ui.Button("Platform Action", 
                             on_click=lambda: print(f"Action performed on {platform}!"),
                             props={"padding": "10px 15px", "background-color": primary_color, "color": "white"}),
                    ui.Button("Universal Action", 
                             on_click=lambda: print("This works everywhere!"),
                             props={"padding": "10px 15px", "background-color": "#27ae60", "color": "white"})
                ],
                props={"spacing": 10, "alignment": "AlignCenter", "margin-top": "20px"}
            ),
            
            ui.Label("This component automatically adapts to the current platform", 
                    props={"margin-top": "20px", "font-size": "12px", "color": "#95a5a6", "text-align": "center"})
        ],
        props={"padding": "40px", "spacing": 15, "alignment": "AlignCenter"}
    )

if __name__ == "__main__":
    # Default to cross-platform app
    winup.run("examples.platform_specific:CrossPlatformApp", title="Platform Demo - WinUp", width=500, height=400, web_title="JSI", platform="web")
