import winup
from winup import ui

def App():
    """
    A test application to showcase the Dock widget.
    """

    # The main content of the window will be the central widget.
    # The Docks will arrange themselves around it.
    main_content = ui.Column(
        props={"alignment": "AlignHCenter", "spacing": 20, "padding": 40},
        children=[
            ui.Label("Main Content Area", props={"font-size": "24px", "font-weight": "bold"}),
            ui.Label("You can dock, float, and close the panels around this central widget."),
        ]
    )

    # Left Dock for tools
    left_dock = ui.Dock(
        props={
            "title": "Tools",
            "area": "left",
            "allowed_areas": ["left", "right"]
        },
        children=[
            ui.Column([
                ui.Button("Tool 1"),
                ui.Button("Tool 2"),
                ui.Button("Tool 3"),
            ], props={"spacing": 10, "padding": 10})
        ]
    )

    # Right Dock for properties
    right_dock = ui.Dock(
        props={
            "title": "Properties",
            "area": "right"
        },
        children=[
            ui.Label("Details about the selected item will appear here.", props={"padding": 10})
        ]
    )
    
    # Bottom Dock for logging
    bottom_dock = ui.Dock(
        props={
            "title": "Output Log",
            "area": "bottom"
        },
        children=[
            ui.Textarea("Log messages will be displayed here...")
        ]
    )
    
    # The main application window implicitly created by `winup.run` will host
    # the docks. The root component returned here will be set as the central widget.
    # The Dock widgets will automatically find the main window and attach themselves.
    return ui.Frame(
        children=[
            left_dock,
            right_dock,
            bottom_dock,
            main_content
        ]
    )

if __name__ == "__main__":
    winup.run(
        main_component_path="dock_test:App",
        title="Dock Widget Test",
        width=800,
        height=600
    ) 