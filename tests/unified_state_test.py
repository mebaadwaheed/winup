
"""
This test demonstrates the unified state management system in WinUp.

You can run this script in two modes:
1. Desktop mode (default): python tests/unified_state_test.py
2. Web mode: python tests/unified_state_test.py web
"""

import sys
import asyncio
from winup import state, run, web, component, ui

# 1. Unified State Definition
# This state object is created once and can be used by both desktop and web components.
counter_state = state.create("counter", initial_value=0)


# 2. Desktop Application Components
def increment_desktop():
    """Desktop event handler."""
    current_value = counter_state.get()
    # For desktop apps, we use the synchronous `set` method.
    counter_state.set(current_value + 1)

@component
def DesktopApp():
    """The main desktop component."""
    
    # Create a label and bind its 'text' property to the counter state.
    # The formatter function determines how the state value is displayed.
    label = ui.Label()
    counter_state.bind_to(label, "text", formatter=lambda count: f"Desktop Counter: {count or 0}")

    # The button triggers the synchronous state update.
    button = ui.Button("Increment", on_click=increment_desktop)
    
    container = ui.Column(children=[label, button])
    return container


# 3. Web Application Components
async def increment_web(event: dict):
    """Web event handler (must be async)."""
    current_value = counter_state.get()
    # For web apps, we use the asynchronous `set_async` method
    # to broadcast the change to all connected clients.
    await counter_state.set_async(current_value + 1)

@web.component
def WebApp():
    """The main web component."""
    return web.ui.Column(
        style={'padding': '2rem', 'gap': '1rem', 'align_items': 'center'},
        children=[
            web.ui.Label("Web Counter", style={'font_size': '1.5rem', 'font_weight': 'bold'}),
            # The `bind_text` prop creates a one-way binding from the state to the label's text.
            web.ui.Label(bind_text="counter", style={'font_size': '2rem'}),
            # The button triggers the asynchronous state update.
            web.ui.Button("Increment", on_click=increment_web)
        ]
    )

# The web router is needed to serve the WebApp component.
router = web.Router({
    "/": WebApp
})


# 4. Main execution block
# This part checks the command-line arguments to decide which app version to run.
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'web':
        print("Running WEB version of the unified state test...")
        print("Access at http://127.0.0.1:8000")
        web.web_run(router_path="unified_state_test:router")
    else:
        print("Running DESKTOP version of the unified state test...")
        run(
            main_component_path="unified_state_test:DesktopApp",
            title="Unified State Desktop Test"
        ) 