# tests/web_test.py
import sys
import os
from typing import Any

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from winup import web
    from winup.web.ui.component import Component # For type hinting if needed
except ImportError:
    print("Please install web dependencies first: pip install .[web]")
    sys.exit(1)

# These functions will be available in the transpiled JS scope.
# Their bodies are never run in Python.
def get_element(element_id: str) -> Any: pass

def handle_mount(el: Component):
    """A Python function that will manipulate another component."""
    print("This message comes from Python's print()!")
    
    target_label = get_element('my-target-label')
    
    # Use Pythonic, snake_case properties:
    target_label.style.color = 'green'
    target_label.style.font_weight = 'bold' # Converted to fontWeight
    
    # Use text_content for safer text updates:
    target_label.text_content = 'I was changed by a Pythonic hook!' # Converted to textContent

@web.component
def App():
    """A demo of the new web layout components."""
    
    # A simple card component for demonstration
    def Card(title: str, content: str):
        return web.ui.Column(
            gap="5px",
            style={
                'padding': '1rem',
                'border': '1px solid #ddd',
                'border_radius': '8px',
                'background_color': '#f9f9f9'
            },
            children=[
                web.ui.Label(title, style={'font_weight': 'bold'}),
                web.ui.Label(content)
            ]
        )

    return web.ui.Column(
        gap="20px",
        style={'padding': '2rem', 'background_color': '#f0f2f5', 'min_height': '100vh'},
        children=[
            web.ui.Label("Web Layout Showcase", style={'font_size': '24px'}),
            
            # --- Row Example ---
            web.ui.Row(
                gap="10px",
                children=[
                    web.ui.Button("Button 1"),
                    web.ui.Button("Button 2"),
                    web.ui.Button("Button 3"),
                ]
            ),
            
            # --- Grid Example ---
            web.ui.Grid(
                gap="10px",
                grid_template_columns="repeat(3, 1fr)", # A 3-column grid
                children=[
                    (Card("Card 1", "Content for card 1"), 0, 0, 1, 1),
                    (Card("Card 2", "Content for card 2"), 0, 1, 1, 1),
                    (Card("Card 3", "Content for card 3"), 0, 2, 1, 1),
                    (Card("Wide Card", "This card spans two columns."), 1, 0, 1, 2),
                ]
            ),

            # --- Stack Example ---
            # In a real app, you would use state to change the active_child_index
            web.ui.Stack(
                active_child_index=0, # Show the first child
                children=[
                    Card("Page 1", "This is the first page of the stack."),
                    Card("Page 2", "This is the second page."),
                ]
            )
        ]
    )

if __name__ == "__main__":
    web.web_run(main_component_path="web_test:App", title="Web Layout Demo")
