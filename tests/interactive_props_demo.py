import winup
from winup import ui

def App():
    # Create a color picker for dynamic styling
    color_picker = ui.ColorPicker(
        selected_color="#1976d2",
        on_change=lambda color: update_theme(color),
        props={"margin": "10px 0"}
    )
    
    # Carousel with multiple slides
    carousel = ui.Carousel(
        children=[
            ui.Label(
                text="Slide 1: Image Widget Test",
                props={"font-size": "18px", "text-align": "center", "padding": "40px"}
            ),
            ui.Label(
                text="Slide 2: All widgets now support props!",
                props={"font-size": "18px", "text-align": "center", "padding": "40px", "color": "#4caf50"}
            ),
            ui.Label(
                text="Slide 3: TreeView shows hierarchical data",
                props={"font-size": "18px", "text-align": "center", "padding": "40px", "color": "#ff9800"}
            )
        ],
        autoplay_ms=3000,
        props={
            "height": "150px",
            "border": "2px solid #ddd",
            "border-radius": "8px",
            "margin": "20px 0"
        }
    )
    
    def update_theme(color):
        print(f"Theme color changed to: {color}")
    
    return ui.Column(children=[
        # Header
        ui.Label(
            text="🎨 Interactive Props Demo",
            props={
                "font-size": "28px",
                "font-weight": "bold",
                "text-align": "center",
                "color": "#1976d2",
                "padding": "20px",
                "background-color": "#e3f2fd",
                "border-radius": "8px",
                "margin": "20px"
            }
        ),
        
        # Color picker section
        ui.Row(children=[
            ui.Label(
                text="Theme Color:",
                props={"font-weight": "bold", "margin-right": "10px"}
            ),
            color_picker
        ], props={"padding": "10px", "background-color": "#f5f5f5"}),
        
        # Carousel demo
        carousel,
        
        # Grid of widgets demonstrating props
        ui.Grid(
            children=[
                # Row 1: (component, row, col, rowspan, colspan)
                (ui.Button(
                    text="Styled Button",
                    props={
                        "background-color": "#4caf50",
                        "color": "white",
                        "border": "none",
                        "padding": "12px 24px",
                        "border-radius": "6px",
                        "font-weight": "bold"
                    }
                ), 0, 0, 1, 1),
                
                (ui.Input(
                    placeholder="Styled input field",
                    props={
                        "border": "2px solid #2196f3",
                        "border-radius": "4px",
                        "padding": "8px",
                        "font-size": "14px"
                    }
                ), 0, 1, 1, 1),
                
                (ui.Checkbox(
                    text="Styled checkbox",
                    props={
                        "color": "#ff5722",
                        "font-weight": "bold"
                    }
                ), 0, 2, 1, 1),
                
                # Row 2
                (ui.Switch(
                    text="Toggle switch",
                    props={
                        "color": "#9c27b0",
                        "margin": "10px 0"
                    }
                ), 1, 0, 1, 1),
                
                (ui.RadioButton(
                    text="Radio option",
                    props={
                        "color": "#607d8b",
                        "font-style": "italic"
                    }
                ), 1, 1, 1, 1),
                
                (ui.Label(
                    text="Styled label",
                    props={
                        "background-color": "#fff3e0",
                        "color": "#e65100",
                        "padding": "8px",
                        "border-radius": "4px",
                        "border": "1px solid #ffcc02"
                    }
                ), 1, 2, 1, 1)
            ],
            props={
                "padding": "20px"
            }
        ),
        
        # Expandable sections
        ui.ExpandablePanel(
            title="📊 Chart Widgets",
            expanded=False,
            header_props={
                "background-color": "#e8f5e8",
                "color": "#2e7d32",
                "font-weight": "bold"
            },
            content_props={
                "background-color": "#f9f9f9",
                "padding": "15px"
            },
            children=[
                ui.ScatterPlot(
                    data={"Dataset": [(1, 2), (3, 4), (5, 6), (7, 8)]},
                    title="Sample Scatter Plot",
                    props={
                        "height": "200px",
                        "border": "1px solid #4caf50"
                    }
                )
            ]
        ),
        
        ui.ExpandablePanel(
            title="🌳 TreeView Demo",
            expanded=False,
            header_props={
                "background-color": "#fff3e0",
                "color": "#e65100",
                "font-weight": "bold"
            },
            content_props={
                "background-color": "#fafafa",
                "padding": "15px"
            },
            children=[
                ui.TreeView(
                    data={
                        "Root": {
                            "Branch 1": ["Leaf 1", "Leaf 2"],
                            "Branch 2": ["Leaf 3", "Leaf 4", "Leaf 5"]
                        },
                        "Another Root": ["Item A", "Item B"]
                    },
                    expanded_nodes={"Root"},
                    on_select=lambda x: print(f"TreeView selected: {x}"),
                    props={
                        "background-color": "white",
                        "border": "1px solid #ff9800",
                        "height": "200px"
                    }
                )
            ]
        ),
        
        # Footer
        ui.Label(
            text="🎉 All widgets fixed and enhanced with full props support!",
            props={
                "background-color": "#e1f5fe",
                "color": "#0277bd",
                "padding": "20px",
                "text-align": "center",
                "font-size": "18px",
                "font-weight": "bold",
                "border-radius": "8px",
                "margin": "20px",
                "border": "2px solid #03a9f4"
            }
        )
    ], props={"padding": "10px", "background-color": "#fafafa"})

if __name__ == "__main__":
    winup.run(main_component_path="interactive_props_demo:App", title="Interactive Props Demo")
