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
            "padding": "12px",
            "border-radius": "8px 8px 0 0"
        },
        content_props={
            "background-color": "#f5f5f5",
            "padding": "15px",
            "border-radius": "0 0 8px 8px"
        },
        children=[
            ui.TreeView(
                data=tree_data,
                expanded_nodes={"Documents", "Documents.Projects"},
                on_select=lambda x: panel.set_title(f"Selected: {x}"),
                height=250,
                width=None,
                props={
                    "background-color": "white",
                    "border": "2px solid #2196f3",
                    "border-radius": "6px",
                    "padding": "8px"
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
            
            # File Explorer Section
            ui.Label(text="🌳 File Explorer with Dynamic Titles:", props={"font-weight": "bold", "font-size": "18px", "margin": "20px 0 10px 0"}),
            panel,
            
            # Controls Section
            ui.Label(text="🎛️ Interactive Controls:", props={"font-weight": "bold", "font-size": "16px", "margin": "15px 0 10px 0"}),
            ui.Row(children=[
                ui.Column(children=[
                    ui.Label(text="Slider Control:", props={"font-weight": "bold", "margin-bottom": "3px", "font-size": "14px"}),
                    ui.Slider(
                        min=0, max=100, value=50,
                        on_change=lambda val: print(f"Slider: {val}"),
                        props={
                            "margin": "3px 0 10px 0",
                            "background-color": "#f0f0f0"
                        }
                    ),
                    
                    ui.Label(text="Progress Bar:", props={"font-weight": "bold", "margin-bottom": "3px", "font-size": "14px"}),
                    ui.ProgressBar(
                        min_val=0, max_val=100, default_val=75,
                        props={
                            "height": "18px",
                            "margin": "3px 0 10px 0"
                        }
                    ),
                    
                    ui.Link(
                        text="📚 Documentation",
                        url="https://github.com/winup",
                        props={
                            "font-size": "14px",
                            "margin": "5px 0",
                            "color": "#1976d2"
                        }
                    )
                ], props={"width": "48%", "margin-right": "2%"}),
                
                ui.Column(children=[
                    ui.Label(text="Feature List:", props={"font-weight": "bold", "margin-bottom": "3px", "font-size": "14px"}),
                    ui.List(
                        items=["✅ TreeView fixed", "✅ Props support", "✅ Dynamic titles"],
                        on_select=lambda item: print(f"Selected: {item}"),
                        height=80,
                        props={
                            "background-color": "white",
                            "border": "1px solid #ccc",
                            "border-radius": "4px",
                            "font-size": "12px"
                        }
                    )
                ], props={"width": "50%"})
            ]),
            
            # Charts Section
            ui.Label(text="📊 Chart Widgets with Props:", props={"font-weight": "bold", "font-size": "18px", "margin": "20px 0 10px 0"}),
            ui.Row(children=[
                ui.BarChart(
                    data=chart_data,
                    title="Quarterly Sales",
                    props={
                        "height": "180px",
                        "width": "32%",
                        "margin-right": "2%",
                        "border": "2px solid #4caf50",
                        "border-radius": "6px",
                        "background-color": "white"
                    }
                ),
                
                ui.LineChart(
                    data=line_data,
                    title="Sales Trend",
                    props={
                        "height": "180px",
                        "width": "32%",
                        "margin-right": "2%",
                        "border": "2px solid #2196f3",
                        "border-radius": "6px",
                        "background-color": "white"
                    }
                ),
                
                ui.PieChart(
                    data=pie_data,
                    title="OS Market Share",
                    props={
                        "height": "180px",
                        "width": "32%",
                        "border": "2px solid #ff9800",
                        "border-radius": "6px",
                        "background-color": "white"
                    }
                )
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
