import winup
from winup import ui

def App():
    panel = ui.ExpandablePanel(
        title="My Panel",
        header_props={
            "vertical-align": "top",
            "background-color": "#f0f0f0",
            "font-weight": "bold"
        },
        content_props={
            "padding": "10px",
            "background-color": "white"
        },
        children=[
            ui.Label(text="Panel content here")
        ]
    )
    
    # Update title dynamically
    def on_selection_change(selected_item):
        panel.set_title(f"Selected: {selected_item}")
    
    return ui.Column(children=[panel])

if __name__ == "__main__":
    winup.run(main_component_path="new_panel:App", title="Expandable Panel Example")
