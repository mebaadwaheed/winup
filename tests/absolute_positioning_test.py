# tests/absolute_positioning_test.py
import winup
from winup import ui, style

# Add some styles for visual clarity
style.add_style_dict({
    "#canvas": {
        "background-color": "#2c3e50",
        "border": "2px solid #bdc3c7",
    },
    ".placed-label": {
        "color": "white",
        "font-weight": "bold",
        "background-color": "rgba(0, 0, 0, 0.3)",
        "padding": "5px",
        "border-radius": "3px"
    },
    "#overlap-label": {
        "background-color": "#e74c3c",
        "color": "white",
        "padding": "10px",
        "border": "2px solid white",
        "font-weight": "bold",
    }
})

@winup.component
def AbsolutePositioningDemo():
    """A component demonstrating the new .place_child() feature."""

    # 1. Create a layout-less Frame to act as the canvas.
    canvas = ui.Frame(props={
        "id": "canvas",
        "min-width": "450px",
        "min-height": "300px",
    })

    # 2. Place various widgets at absolute coordinates.
    canvas.place_child(
        ui.Label("Placed at (20, 20)", props={"class": "placed-label"}),
        x=20, y=20
    )
    
    canvas.place_child(
        ui.Button("A Button at (50, 60)"),
        x=50, y=60, width=180, height=30
    )

    canvas.place_child(
        ui.Checkbox("A Checkbox at (80, 110)"),
        x=80, y=110
    )

    # 3. Demonstrate overlapping elements.
    canvas.place_child(
        ui.Label("OVERLAP", props={"id": "overlap-label"}),
        x=70, y=80, width=150, height=50
    )

    # 4. Demonstrate the error case.
    def test_error_case():
        # To test the error, we create a dummy frame with a layout on the fly.
        # It's created here inside the handler so it won't appear as a floating window.
        frame_with_layout = ui.Frame(layout="vertical")
        try:
            frame_with_layout.place_child(ui.Label("This will fail"), x=0, y=0)
        except RuntimeError as e:
            print("\n--- EXPECTED ERROR CAUGHT ---")
            print(e)
            print("-----------------------------")

    error_button = ui.Button(
        "Try to .place_child() on a Frame with a layout (will error)",
        on_click=test_error_case
    )
    
    # Add the button to the main canvas
    canvas.place_child(error_button, x=20, y=250, width=410, height=40)

    return canvas


if __name__ == "__main__":
    winup.run(main_component_path="absolute_positioning_test:AbsolutePositioningDemo", title="Absolute Positioning (.place_child) Demo") 