# tests/layout_test.py
import winup
from winup import ui, style

style.add_style_dict({
    ".test-frame": {
        "border": "1px solid $border-color",
        "background-color": "$secondary-color",
        "border-radius": "4px",
    },
    ".label-box": {
        "background-color": "$primary-color",
        "color": "$primary-text-color",
        "padding": "10px",
        "font-weight": "bold",
        "border-radius": "4px",
    }
})

@winup.component
def LayoutDemo():
    """A component demonstrating the new advanced layout options."""
    
    # --- Stack Layout Demo ---
    stack = ui.Stack(
        children=[
            ui.Label("This is the first page of the stack.", props={"class": "label-box"}),
            ui.Label("And this is the SECOND page.", props={"class": "label-box"}),
            ui.Button("Page 3!", on_click=lambda: stack.set_current_index(0)),
        ]
    )
    
    stack_controls = ui.Row(
        props={"spacing": 10},
        children=[
            ui.Button("Page 1", on_click=lambda: stack.set_current_index(0)),
            ui.Button("Page 2", on_click=lambda: stack.set_current_index(1)),
            ui.Button("Page 3", on_click=lambda: stack.set_current_index(2)),
        ]
    )

    stack_section = ui.Column(props={"class": "test-frame", "padding": "10px", "spacing": 10}, children=[
        ui.Label("Stack Layout", props={"font-weight": "bold"}),
        stack,
        stack_controls
    ])

    # --- Grid Layout Demo ---
    grid_section = ui.Column(props={"class": "test-frame", "padding": "10px", "spacing": 10}, children=[
        ui.Label("Grid Layout", props={"font-weight": "bold"}),
        ui.Grid(
            props={"spacing": 10},
            children=[
                (ui.Label("R0, C0", props={"class":"label-box"}), 0, 0),
                (ui.Label("R0, C1", props={"class":"label-box"}), 0, 1),
                (ui.Label("R1, C0-C1 (span)", props={"class":"label-box"}), 1, 0, 1, 2),
                (ui.Label("R2, C1", props={"class":"label-box"}), 2, 1),
            ]
        )
    ])

    # --- Flexbox (Stretch) Demo ---
    stretch_section = ui.Column(props={"class": "test-frame", "padding": "10px", "spacing": 10}, children=[
        ui.Label("Row/Column Stretch (Flexbox)", props={"font-weight": "bold"}),
        ui.Row(
            props={"spacing": 5, "min-height": 60},
            children=[
                (ui.Label("1x", props={"class": "label-box"}), {"stretch": 1}),
                (ui.Label("2x", props={"class": "label-box"}), {"stretch": 2}),
                (ui.Label("1x", props={"class": "label-box"}), {"stretch": 1}),
            ]
        )
    ])

    return ui.Column(
        props={"spacing": 20, "margin": 15},
        children=[stack_section, grid_section, stretch_section]
    )


if __name__ == "__main__":
    winup.run(main_component_path="layout_test:LayoutDemo", title="Advanced Layouts Demo", dev = True) 