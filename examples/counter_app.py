"""
Counter App Example - Stateful Cross-Platform Component

This example demonstrates proper state management using WinUp's state system
in a unified component that works on both desktop and web platforms.

Usage:
    # Desktop mode
    winup run examples.counter_app:CounterApp --desktop
    
    # Web mode  
    winup run examples.counter_app:CounterApp --web --web-port 8001
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, component, state
from winup.core.platform import get_current_platform

# Create a global state for the counter
counter_state = state.create("counter", initial_value=0)

@component(web=True, desktop=True)
def CounterApp():
    """A counter app with increment/decrement functionality using WinUp state."""
    platform = get_current_platform()
    
    def increment():
        current = counter_state.get()
        counter_state.set(current + 1)
        print(f"Count incremented to: {counter_state.get()}")
    
    def decrement():
        current = counter_state.get()
        counter_state.set(current - 1)
        print(f"Count decremented to: {counter_state.get()}")
    
    def reset():
        counter_state.set(0)
        print("Count reset to 0")
    
    # Create the counter display label
    counter_label = ui.Label("Count: 0", 
                           props={"font-size": "32px", "font-weight": "bold", "margin": "30px 0", "color": "#e74c3c"})
    
    # Bind the counter state to the label's text property
    counter_state.bind_to(counter_label, "text", formatter=lambda count: f"Count: {count}")
    
    return ui.Column(
        children=[
            ui.Label("🔢 Counter App", 
                    props={"font-size": "24px", "font-weight": "bold", "color": "#2c3e50"}),
            ui.Label(f"Platform: {platform}", 
                    props={"font-size": "14px", "color": "#7f8c8d", "margin-top": "5px"}),
            
            # Counter display - reactively bound to state
            counter_label,
            
            # Button controls
            ui.Row(
                children=[
                    ui.Button("➖ Decrement", 
                             on_click=decrement,
                             props={"padding": "10px 15px", "background-color": "#e74c3c", "color": "white", "margin-right": "10px"}),
                    ui.Button("🔄 Reset", 
                             on_click=reset,
                             props={"padding": "10px 15px", "background-color": "#95a5a6", "color": "white", "margin": "0 10px"}),
                    ui.Button("➕ Increment", 
                             on_click=increment,
                             props={"padding": "10px 15px", "background-color": "#27ae60", "color": "white", "margin-left": "10px"})
                ],
                props={"alignment": "AlignCenter", "spacing": 5}
            ),
            
            ui.Label("Click buttons to change the counter value", 
                    props={"margin-top": "20px", "font-size": "12px", "color": "#7f8c8d"})
        ],
        props={"padding": "40px", "spacing": 15, "alignment": "AlignCenter"}
    )

if __name__ == "__main__":
    winup.run("examples.counter_app:CounterApp", title="Counter App - WinUp", width=450, height=400)
