import winup
from winup import ui, component

@component
def App():
    # Sample data for widgets
    tree_data = {
        "Documents": {
            "Projects": ["WinUp", "MyApp", "WebSite"],
            "Personal": ["Resume.pdf", "Photos", "Notes.txt"]
        },
        "Downloads": ["installer.exe", "music.mp3", "video.mp4"],
        "Desktop": ["shortcut1", "shortcut2"]
    }
    
    chart_data = {"Q1": 25, "Q2": 40, "Q3": 35, "Q4": 50}
    line_data = {"Sales": [(1, 20), (2, 35), (3, 25), (4, 45), (5, 60)]}
    pie_data = {"Windows": 45, "macOS": 25, "Linux": 30}
    
    # Create expandable panel with dynamic title updates
    panel = ui.ExpandablePanel(
        title="File Explorer",
        expanded=True,
        header_props={
            "background-color": "#e3f2fd",
            "font-weight": "bold",
            "padding": "12px"
        },
        content_props={
            "background-color": "#f5f5f5",
            "padding": "10px"
        },
        children=[
            ui.TreeView(
                data=tree_data,
                expanded_nodes={"Documents", "Documents.Projects"},
                on_select=lambda x: panel.set_title(f"Selected: {x}"),
                props={
                    "background-color": "white",
                    "border": "1px solid #ddd"
                }
            )
        ]
    )
    
    return ui.Column(
        children=[
            # Header
            ui.Label(
                text="🧪 WinUp Widget Test Suite - All Fixed Features",
                props={
                    "font-size": "24px",
                    "font-weight": "bold",
                    "color": "#1976d2",
                    "padding": "20px",
                    "text-align": "center"
                }
            ),
            
            # Main content in rows
            ui.Row(children=[
                # Left column - File explorer and controls
                ui.Column(children=[
                    panel,
                    
                    ui.Label(text="Interactive Controls:", props={"font-weight": "bold", "margin-top": "20px"}),
                    
                    # Slider with props
                    ui.Slider(
                        min=0, max=100, value=50,
                        on_change=lambda val: print(f"Slider: {val}"),
                        props={
                            "margin": "10px 0",
                            "background-color": "#f0f0f0"
                        }
                    ),
                    
                    # Progress bar with props
                    ui.ProgressBar(
                        min_val=0, max_val=100, default_val=75,
                        props={
                            "height": "20px",
                            "border-radius": "10px",
                            "background-color": "#e0e0e0"
                        }
                    ),
                    
                    # Link with props
                    ui.Link(
                        text="Visit WinUp Documentation",
                        url="https://github.com/winup",
                        props={
                            "font-size": "16px",
                            "margin": "10px 0",
                            "color": "#1976d2"
                        }
                    ),
                    
                    # List widget
                    ui.List(
                        items=["Feature 1: TreeView fixed", "Feature 2: Props support", "Feature 3: Dynamic titles"],
                        on_select=lambda item: print(f"Selected: {item}"),
                        props={
                            "background-color": "white",
                            "border": "1px solid #ccc",
                            "margin": "10px 0"
                        }
                    )
                ], props={"width": "50%", "padding": "10px"}),
                
                # Right column - Charts and image
                ui.Column(children=[
                    ui.Label(text="Chart Widgets with Props:", props={"font-weight": "bold"}),
                    
                    # Bar chart
                    ui.BarChart(
                        data=chart_data,
                        title="Quarterly Sales",
                        props={
                            "height": "200px",
                            "margin": "10px 0",
                            "border": "1px solid #ddd"
                        }
                    ),
                    
                    # Line chart
                    ui.LineChart(
                        data=line_data,
                        title="Sales Trend",
                        props={
                            "height": "200px",
                            "margin": "10px 0",
                            "border": "1px solid #ddd"
                        }
                    ),
                    
                    # Pie chart
                    ui.PieChart(
                        data=pie_data,
                        title="OS Market Share",
                        props={
                            "height": "200px",
                            "margin": "10px 0",
                            "border": "1px solid #ddd"
                        }
                    )
                ], props={"width": "50%", "padding": "10px"})
            ]),
            
            # Footer with status
            ui.Label(
                text="✅ All widgets now support props parameter • TreeView shows hierarchical data • ExpandablePanel has dynamic titles",
                props={
                    "background-color": "#e8f5e8",
                    "color": "#2e7d32",
                    "padding": "15px",
                    "border-radius": "5px",
                    "margin": "20px",
                    "text-align": "center"
                }
            )
        ],
        props={
            "background-color": "#fafafa",
            "min-height": "100vh"
        }
    )

if __name__ == "__main__":
    winup.run(main_component_path="comprehensive_widget_test:App", title="WinUp Widget Test Suite")
