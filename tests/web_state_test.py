import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from winup import web, state

# --- 1. Create State Variables ---
# This is the global state for your application
counter = state.create("counter", 0)
username = state.create("username", "Guest")

# --- 2. Define Event Handlers at the top level ---
async def increment(event):
    """
    Gets the current value of the counter, increments it, and sets it.
    This will automatically broadcast the change to all clients.
    """
    current_value = counter.get()
    await counter.set_async(current_value + 1)

# --- 3. Define Components ---
@web.component
def App():
    return web.ui.Column(
        gap="1rem",
        style={'max_width': '600px', 'margin': '2rem auto'},
        children=[
            web.ui.Label(
                # This label's text will automatically update
                # when the 'counter' state changes.
                bind_text="counter",
                style={'font_size': '2rem', 'font_weight': 'bold'}
            ),
            web.ui.Button(
                "Increment",
                # Note: Click handlers that modify state should be async
                on_click=increment 
            ),
            web.ui.Input(
                # This input has two-way binding to the 'username' state.
                # Typing in the box updates the server state, which updates
                # all other bound elements.
                bind_value="username"
            ),
            web.ui.Label(
                # This label is also bound to the 'username' state
                # and will update as you type in the input above.
                bind_text="username",
                style={'font_style': 'italic'}
            )
        ]
    )

if __name__ == "__main__":
    web.web_run(main_component_path="web_state_test:App", title="Web State Demo")
