import sys
import os
import random

# Add project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, state, style

# --- Part 1: Random File Finder Logic ---
def find_and_set_random_file(path_state):
    """Finds a random file in the project and updates the application state."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    all_paths = [os.path.join(root, name) for root, dirs, files in os.walk(project_root) for name in dirs + files]
    path_state.set(random.choice(all_paths) if all_paths else "No files found.")

# --- Part 2: Main Application Component ---

def ShowcaseApp():
    """The main component for the feature showcase application."""
    
    # --- State Initialization ---
    random_path = state.create('random_path', 'Click the button!')
    email_value = state.create('email_value', 'not-an-email')
    name_value = state.create('name_value', 'John Doe')

    # --- Random File Finder UI ---
    random_path_label = ui.Label()
    random_path.bind_to(random_path_label, 'text', lambda p: p) # Bind to the state object

    random_file_finder = ui.Column(props={"spacing": 5}, children=[
        ui.Label("Random File Finder", props={"font-size": "16px", "font-weight": "bold"}),
        random_path_label,
        ui.Button("Find Random File", on_click=lambda: find_and_set_random_file(random_path))
    ])

    # --- Two-Way Binding & Validation UI ---
    email_input = ui.Input(props={"placeholder": "Enter your email", "validation": "email"})
    # Two-way binding still uses the manager directly for now.
    state.bind_two_way(email_input, 'email_value')

    email_mirror_label = ui.Label()
    email_value.bind_to(email_mirror_label, 'text', lambda v: f"Live email state: {v}")

    name_input = ui.Input(props={"placeholder": "Name (must be > 10 chars)", "validation": lambda text: len(text) > 10})
    state.bind_two_way(name_input, 'name_value')

    name_mirror_label = ui.Label()
    # Using bind_to is cleaner than state.subscribe + label.set_text
    name_value.bind_to(name_mirror_label, 'text', lambda v: f"Live name state: {v}")

    form = ui.Column(props={"spacing": 5}, children=[
        ui.Label("Two-Way Binding & Validation", props={"font-size": "16px", "font-weight": "bold"}),
        ui.Label("Email:"), email_input,
        ui.Label("Email state (live):"), email_mirror_label,
        ui.Label("Name:"), name_input,
        ui.Label("Name state (live):"), name_mirror_label
    ])

    # --- Final Layout ---
    return ui.Column(props={"spacing": 20, "margin": "20px"}, children=[
        random_file_finder, 
        form,
        ui.ExpandablePanel(
            "Expandable Panel",
            children=[
                ui.Column(props={"spacing": 10}, children=[
                    ui.Label("This is inside the expandable panel!"),
                    ui.Input(props={"placeholder": "You can put widgets here"})
                ])
            ]
        ),
        ui.Carousel(
            children=[
                ui.Label("Page 1", props={"background-color": "#f0f0f0", "alignment": "AlignCenter", "height": 100}),
                ui.Label("Page 2", props={"background-color": "#e0e0e0", "alignment": "AlignCenter", "height": 100}),
           ui.Label("Page 3", props={"background-color": "#d0d0d0", "alignment": "AlignCenter", "height": 100}),
            ]
        )
    ])

if __name__ == "__main__":
    # Add validation styles to the default styler
    style.add_style_dict({
        "QLineEdit.valid": {"border": "2px solid #28a745"},
        "QLineEdit.invalid": {"border": "2px solid #dc3545"}
    })
    
    winup.run(
        main_component_path="showcase:ShowcaseApp",
        title="WinUp Feature Showcase",
        width=800,
        height=600
    )