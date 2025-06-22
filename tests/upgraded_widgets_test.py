import winup
from winup import ui

def App():
    """
    A test application to showcase the newly upgraded and more
    customizable Carousel and ExpandablePanel widgets.
    """

    # --- 1. Upgraded ExpandablePanel ---
    custom_panel = ui.ExpandablePanel(
        title="Customized Expandable Panel",
        expanded=True,  # Start in the expanded state
        animation_duration=200,  # Faster animation
        expand_icon="✨",
        collapse_icon="👌",
        header_props={
            "background-color": "#e3f2fd",
            "color": "#1e88e5",
            "font-weight": "bold",
            "border-radius": "5px"
        },
        content_props={
            "background-color": "#fafafa",
            "border": "1px solid #e3f2fd",
            "padding": "15px"
        },
        children=[
            ui.Label("This content area has custom styling!")
        ]
    )

    # --- 2. Upgraded Carousel ---
    custom_carousel = ui.Carousel(
        animation_duration=600,  # Slower, more deliberate animation
        autoplay_ms=3000,  # Autoplay every 3 seconds
        show_nav_buttons=True,
        show_indicators=True,
        nav_button_props={
            "background-color": "rgba(0, 0, 0, 0.3)",
            "color": "white",
            "border": "none",
            "border-radius": "15px",
            "font-size": "16px",
            "font-weight": "bold",
            "min-width": "30px",
            "min-height": "30px"
        },
        indicator_props={
            "background-color": "#ccc",
            "border-radius": "5px"
        },
        children=[
            ui.Frame(props={"background-color": "#ffadad"}, children=[ui.Label("Slide 1")]),
            ui.Frame(props={"background-color": "#ffd6a5"}, children=[ui.Label("Slide 2")]),
            ui.Frame(props={"background-color": "#fdffb6"}, children=[ui.Label("Slide 3")]),
            ui.Frame(props={"background-color": "#caffbf"}, children=[ui.Label("Slide 4")]),
        ]
    )


    # --- 3. Main Layout ---
    return ui.Column(
        children=[
            ui.Label("Upgraded Widgets Demo", props={"font-size": "24px", "font-weight": "bold"}),
            custom_panel,
            custom_carousel,
        ],
        props={"spacing": 20, "padding": "20px"}
    )


if __name__ == "__main__":
    winup.run(
        main_component_path="upgraded_widgets_test:App",
        title="Upgraded Widgets Test",
        width=600,
        height=500
    ) 