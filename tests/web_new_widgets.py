# tests/web_new_widgets.py
import sys
import os
from typing import Any

# Add project root to path for local testing
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from winup import web
    from winup.web.ui.component import Component # For type hinting
except ImportError:
    print("Please install web dependencies first: pip install .[web]")
    sys.exit(1)

# --- 1. Mocks and Helpers ---
def get_element(element_id: str) -> Any: pass

# --- 2. State Management ---
counter = web.state.create("counter", 0)
text_input = web.state.create("text_input", "Hello WinUp!")
is_checked = web.state.create("is_checked", False)
checked_status_text = web.state.create("checked_status_text", "The checkbox is currently: Unchecked")

# --- 3. Event Handlers ---
async def increment(event):
    await counter.set(counter.get() + 1)

async def toggle_checkbox(event):
    new_value = not is_checked.get()
    await is_checked.set(new_value)
    status = "Checked" if new_value else "Unchecked"
    await checked_status_text.set(f"The checkbox is currently: {status}")

# --- 4. Lifecycle Hooks ---
def on_page_mount(el: Component):
    print("State and Hooks Page Mounted! Check the browser console.")
    title = get_element('state-title')
    title.style.color = 'darkorchid'
    title.style.font_style = 'italic'

# --- 5. Reusable Components ---
def Card(title: str, children: list, props: dict = {}):
    """A simple, reusable card component for styling."""
    default_style = {
        'padding': '1rem', 'border': '1px solid #ddd', 'border_radius': '8px', 'background_color': '#f9f9f9', 'margin_bottom': '1rem'
    }
    final_props = props.copy()
    final_props['style'] = default_style | props.get('style', {})
    
    return web.ui.Column(
        gap="10px",
        props=final_props,
        children=[
            web.ui.Label(title, style={'font_weight': 'bold', 'font_size': '1.2rem'}),
            *children
        ]
    )

# --- 6. Page Components ---
@web.component
def LayoutsPage():
    """A page demonstrating all available layout components."""
    return web.ui.Column(
        gap="20px",
        style={'padding': '2rem'},
        children=[
            web.ui.Label("Layouts Showcase", style={'font_size': '1.5em', 'margin_bottom': '1rem'}),
            Card("Row Layout", children=[web.ui.Row(gap="10px", children=[web.ui.Button("One"), web.ui.Button("Two"), web.ui.Button("Three")])]),
            Card("Grid Layout", children=[
                web.ui.Grid(
                    gap="10px",
                    grid_template_columns="repeat(3, 1fr)",
                    children=[
                        (web.ui.Label("R1, C1"), 0, 0, 1, 1), (web.ui.Label("R1, C2"), 0, 1, 1, 1), (web.ui.Label("R1, C3"), 0, 2, 1, 1),
                        (web.ui.Label("R2, C1-C3 (span)"), 1, 0, 1, 3),
                    ]
                )
            ]),
            Card("Stack Layout", children=[
                web.ui.Label("Note: Stack is best used with state to toggle `active_child_index`."),
                web.ui.Stack(active_child_index=0, style={'padding': '1rem', 'border': '1px dashed grey'}, children=[
                    web.ui.Button("Layer 1 (Visible)"), web.ui.Button("Layer 2 (Hidden)"),
                ])
            ]),
        ]
    )

@web.component
def WidgetsPage():
    """A page demonstrating the new UI widgets."""
    return web.ui.Column(
        gap="20px",
        style={'padding': '2rem'},
        children=[
            web.ui.Label("New Widgets Showcase", style={'font_size': '1.5em', 'margin_bottom': '1rem'}),
            Card("Link & Image", children=[
                web.ui.Link("Visit python.org", href="https://python.org", props={'target': '_blank'}),
                web.ui.Image(src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png", style={'width': '200px', 'margin_top': '1rem'})
            ]),
            Card("BulletedList", children=[web.ui.BulletedList(children=[web.ui.Label("Item 1"), web.ui.Label("Item 2")])]),
            Card("ScrollView", children=[
                web.ui.ScrollView(style={'height': '150px'}, children=[web.ui.Label(f"Line item #{i}") for i in range(30)])
            ]),
        ]
    )

@web.component
def StateAndHooksPage():
    """A page for testing state binding and lifecycle hooks."""
    return web.ui.Column(
        gap="1rem",
        style={'padding': '2rem'},
        props={'on_mount': on_page_mount},
        children=[
            web.ui.Label("State & Hooks", props={'id': 'state-title'}, style={'font_size': '1.5em', 'margin_bottom': '1rem'}),
            Card("Counter", children=[web.ui.Label(bind_text="counter", style={'font_size': '2rem'}), web.ui.Button("Increment", on_click=increment)]),
            Card("Two-Way Binding", children=[
                web.ui.Input(bind_value="text_input"),
                web.ui.Label(bind_text="text_input", style={'font_family': 'monospace', 'margin_top': '0.5rem'}),
            ]),
            Card("Checkbox State", children=[
                web.ui.Row(gap="10px", style={'align_items': 'center'}, children=[
                    web.ui.CheckBox(bind_checked="is_checked", on_change=toggle_checkbox), web.ui.Label("Toggle Me")
                ]),
                web.ui.Label(bind_text="checked_status_text", style={'margin_top': '0.5rem'})
            ]),
        ]
    )
    
@web.component
def HomePage():
    """The main landing page of the application, which includes navigation."""
    return web.ui.Column(
        children=[
            web.ui.Row(
                gap="1.5rem",
                style={'padding': '1rem 2rem', 'background_color': '#333'},
                children=[
                    web.ui.Link("Home", href="/", style={'color': 'white', 'text_decoration': 'none'}),
                    web.ui.Link("Layouts", href="/layouts", style={'color': 'white', 'text_decoration': 'none'}),
                    web.ui.Link("Widgets", href="/widgets", style={'color': 'white', 'text_decoration': 'none'}),
                    web.ui.Link("State & Hooks", href="/state", style={'color': 'white', 'text_decoration': 'none'}),
                ]
            ),
            web.ui.Column(
                style={'padding': '2rem', 'align_items': 'center'},
                children=[
                    web.ui.Label("Welcome to the WinUp Web Test Suite!", style={'font_size': '2em'}),
                    web.ui.Label("Select a page from the navigation bar to see the features in action."),
                ]
            )
        ]
    )


# --- 7. Router Definition ---
# A dictionary mapping URL paths to the component functions that render them.
# The server will render the content of the HomePage for the root path.
# Other pages will be rendered when their path is visited.
router = web.Router(
    routes={
        '/': HomePage,
        '/layouts': LayoutsPage,
        '/widgets': WidgetsPage,
        '/state': StateAndHooksPage,
    }
)

# --- 8. Run the App ---
if __name__ == "__main__":
    web.web_run(router_path="web_new_widgets:router", title="Comprehensive Web Test") 