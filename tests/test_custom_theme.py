#!/usr/bin/env python3
"""
Test script to demonstrate the correct way to add custom themes in WinUp.
This shows both approaches: adding themes in the component and adding them after app start.
"""

import winup
from winup import ui, style

def App():
    """Main application component demonstrating custom themes."""
    
    # Option 1: Add themes in the component (Recommended approach)
    matrix_theme = {
        "primary-color": "#00FF41",
        "primary-text-color": "#000000",
        "background-color": "#0D0208",
        "text-color": "#00FF41",
        "border-color": "#008F11",
        "hover-color": "#00A62A",
        "secondary-color": "#1A1A1A",
        "secondary-text-color": "#00FF41",
        "disabled-color": "#333333",
        "error-color": "#FF4136",
    }
    
    # Add the custom theme
    style.themes.add_theme("matrix", matrix_theme)
    
    def cycle_themes():
        """Cycle through available themes."""
        current_theme = style.themes.get_active_theme_name()
        available_themes = style.themes.get_available_themes()
        
        # Find the next theme in the cycle
        current_index = available_themes.index(current_theme)
        next_index = (current_index + 1) % len(available_themes)
        next_theme = available_themes[next_index]
        
        style.themes.set_theme(next_theme)
        print(f"Switched to theme: {next_theme}")
    
    def add_sunset_theme():
        """Option 2: Add a new theme after the app is running."""
        sunset_theme = {
            "primary-color": "#FF6B35",
            "primary-text-color": "#FFFFFF",
            "background-color": "#2C1810",
            "text-color": "#FFE5D9",
            "border-color": "#8B4513",
            "hover-color": "#FF8C42",
            "secondary-color": "#4A2E20",
            "secondary-text-color": "#FFE5D9",
            "disabled-color": "#5A3D31",
            "error-color": "#FF4136",
        }
        
        style.themes.add_theme("sunset", sunset_theme)
        style.themes.set_theme("sunset")
        print("Added and switched to sunset theme!")
    
    return ui.Column(
        props={"spacing": 15, "margin": "20px"},
        children=[
            ui.Label("Custom Theme Demo", props={"font-size": "24px", "font-weight": "bold"}),
            ui.Label("This demonstrates the correct way to add custom themes in WinUp."),
            
            ui.Row(
                props={"spacing": 10},
                children=[
                    ui.Button("Cycle Themes", on_click=cycle_themes),
                    ui.Button("Add Sunset Theme", on_click=add_sunset_theme),
                ]
            ),
            
            ui.Label("Current theme: ", props={"font-weight": "bold"}),
            ui.Label("Available themes: " + ", ".join(style.themes.get_available_themes())),
            
            # Demo widgets to show theme changes
            ui.Frame(
                props={
                    "background-color": "$background-color",
                    "border": "2px solid $border-color",
                    "padding": "15px",
                    "border-radius": "8px"
                },
                children=[
                    ui.Label("This frame uses theme variables", props={"color": "$text-color"}),
                    ui.Button(
                        "Themed Button",
                        props={
                            "background-color": "$primary-color",
                            "color": "$primary-text-color",
                            "padding": "10px 20px",
                            "border-radius": "5px"
                        }
                    )
                ]
            )
        ]
    )

if __name__ == "__main__":
    winup.run(
        main_component_path="test_custom_theme:App",
        title="Custom Theme Demo",
        width=600,
        height=500,
        dev=True
    ) 