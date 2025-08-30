import winup
from winup import ui

def App():
    """
    Comprehensive test showcasing all the widget fixes and enhancements made:
    - TreeView: Fixed props parameter + hierarchical data support
    - ExpandablePanel: Added props parameter + dynamic title updates
    - Image: Fixed props parameter
    - All graph widgets: Added props parameter + styling support
    - Slider, ProgressBar, Link: Added props parameter + styling support
    - List, ColorPicker, Carousel: Added props parameter
    """
    
    # Counter for dynamic updates
    counter = {"value": 0}
    
    # Create main expandable panel that will update its title
    main_panel = ui.ExpandablePanel(
        title="🔧 Widget Fixes Showcase",
        expanded=True,
        header_props={
            "background-color": "#1976d2",
            "color": "white",
            "font-weight": "bold",
            "padding": "15px",
            "border-radius": "8px 8px 0 0"
        },
        content_props={
            "background-color": "#f8f9fa",
            "padding": "20px",
            "border-radius": "0 0 8px 8px"
        }
    )
    
    def update_counter():
        counter["value"] += 1
        main_panel.set_title(f"🔧 Widget Fixes Showcase (Updates: {counter['value']})")
        print(f"Counter updated to: {counter['value']}")
    
    # TreeView with complex hierarchical data
    tree_data = {
        "Fixed Widgets": {
            "Core Widgets": ["TreeView", "ExpandablePanel", "Image"],
            "Form Controls": ["Slider", "ProgressBar", "Link"],
            "Data Widgets": ["List", "ColorPicker"],
            "Layout Widgets": ["Carousel"]
        },
        "Graph Widgets": {
            "Charts": ["BarChart", "LineChart", "PieChart"],
            "Plots": ["ScatterPlot"]
        },
        "New Features": ["Props parameter support", "Dynamic title updates", "Hierarchical TreeView"]
    }
    
    # Sample data for charts
    performance_data = {"Before Fix": 20, "After Fix": 95, "User Satisfaction": 88}
    trend_data = {"Progress": [(1, 10), (2, 30), (3, 60), (4, 85), (5, 95)]}
    
    # Build the main content
    main_content = [
        # Status banner
        ui.Label(
            text="✅ ALL WIDGETS FIXED - Props parameter added to every widget",
            props={
                "background-color": "#4caf50",
                "color": "white",
                "padding": "12px",
                "text-align": "center",
                "font-weight": "bold",
                "border-radius": "6px",
                "margin-bottom": "20px"
            }
        ),
        
        # Interactive section
        ui.Row(children=[
            ui.Column(children=[
                ui.Label(text="🌳 TreeView with Hierarchical Data:", props={"font-weight": "bold", "margin-bottom": "10px"}),
                ui.TreeView(
                    data=tree_data,
                    expanded_nodes={"Fixed Widgets", "Fixed Widgets.Core Widgets"},
                    on_select=lambda x: print(f"Selected: {x}") or main_panel.set_title(f"Selected: {x}"),
                    props={
                        "background-color": "white",
                        "border": "2px solid #2196f3",
                        "border-radius": "6px",
                        "height": "250px"
                    }
                ),
                
                ui.Label(text="🎛️ Interactive Controls:", props={"font-weight": "bold", "margin": "20px 0 10px 0"}),
                
                ui.Button(
                    text="Update Counter",
                    on_click=update_counter,
                    props={
                        "background-color": "#ff5722",
                        "color": "white",
                        "border": "none",
                        "padding": "10px 20px",
                        "border-radius": "5px",
                        "font-weight": "bold",
                        "margin-bottom": "10px"
                    }
                ),
                
                ui.Slider(
                    min=0, max=100, value=75,
                    on_change=lambda val: print(f"Slider value: {val}"),
                    props={
                        "margin": "10px 0",
                        "background-color": "#e3f2fd"
                    }
                ),
                
                ui.ProgressBar(
                    min_val=0, max_val=100, default_val=85,
                    props={
                        "height": "25px",
                        "border-radius": "12px",
                        "background-color": "#e8f5e8",
                        "margin": "10px 0"
                    }
                )
            ], props={"width": "50%", "padding-right": "10px"}),
            
            ui.Column(children=[
                ui.Label(text="📊 Chart Widgets with Props:", props={"font-weight": "bold", "margin-bottom": "10px"}),
                
                ui.BarChart(
                    data=performance_data,
                    title="Fix Impact Analysis",
                    props={
                        "height": "180px",
                        "border": "2px solid #4caf50",
                        "border-radius": "8px",
                        "margin-bottom": "15px",
                        "background-color": "white"
                    }
                ),
                
                ui.LineChart(
                    data=trend_data,
                    title="Development Progress",
                    props={
                        "height": "180px",
                        "border": "2px solid #2196f3",
                        "border-radius": "8px",
                        "background-color": "white"
                    }
                )
            ], props={"width": "50%", "padding-left": "10px"})
        ]),
        
        # Additional widgets showcase
        ui.Label(text="🎨 Additional Fixed Widgets:", props={"font-weight": "bold", "margin": "30px 0 15px 0"}),
        
        ui.Row(children=[
            ui.ColorPicker(
                selected_color="#9c27b0",
                on_change=lambda color: print(f"Color selected: {color}"),
                props={"margin-right": "15px"}
            ),
            
            ui.Link(
                text="Documentation Link",
                url="https://github.com/winup",
                props={
                    "color": "#1976d2",
                    "font-size": "16px",
                    "margin-right": "15px"
                }
            ),
            
            ui.List(
                items=["Props support added", "TreeView hierarchy fixed", "Dynamic titles working"],
                selected_index=0,
                on_select=lambda item: print(f"List item: {item}"),
                height=100,
                props={
                    "background-color": "white",
                    "border": "1px solid #ddd",
                    "border-radius": "4px"
                }
            )
        ]),
        
        # Carousel demo
        ui.Label(text="🎠 Carousel Widget:", props={"font-weight": "bold", "margin": "20px 0 10px 0"}),
        ui.Carousel(
            children=[
                ui.Label(text="Slide 1: All widgets now support props!", props={"text-align": "center", "padding": "30px", "font-size": "18px"}),
                ui.Label(text="Slide 2: TreeView shows hierarchical data", props={"text-align": "center", "padding": "30px", "font-size": "18px", "color": "#4caf50"}),
                ui.Label(text="Slide 3: ExpandablePanel has dynamic titles", props={"text-align": "center", "padding": "30px", "font-size": "18px", "color": "#ff5722"})
            ],
            autoplay_ms=4000,
            props={
                "height": "120px",
                "border": "2px solid #9c27b0",
                "border-radius": "8px",
                "background-color": "#f3e5f5"
            }
        ),
        
        # Summary
        ui.Label(
            text="🎉 Summary: Fixed 'unexpected keyword argument props' error in v2.5.6 by adding props parameter to all widgets. Enhanced TreeView with hierarchical data support and ExpandablePanel with dynamic title updates.",
            props={
                "background-color": "#e8f5e8",
                "color": "#2e7d32",
                "padding": "20px",
                "border-radius": "8px",
                "margin-top": "30px",
                "font-size": "16px",
                "line-height": "1.5",
                "border": "2px solid #4caf50"
            }
        )
    ]
    
    # Add content to main panel
    for widget in main_content:
        main_panel.add_child(widget)
    
    return ui.Column(children=[
        main_panel
    ], props={
        "padding": "20px",
        "background-color": "#f5f5f5",
        "min-height": "100vh"
    })

if __name__ == "__main__":
    winup.run(main_component_path="widget_fixes_showcase:App", title="WinUp Widget Fixes Showcase")
