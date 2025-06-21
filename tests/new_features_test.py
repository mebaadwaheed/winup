import winup
from winup import ui, traits, state

# --- 1. Define Components for each Tab ---

def create_widgets_demo_tab():
    """This component demonstrates the new widgets."""
    
    # Create state objects for the switch and combobox
    switch_status = state.create("switch_status", "OFF")
    combo_selection = state.create("combo_selection", "Item 1")

    status_label = ui.Label("")
    
    # Bind the label's text to both state objects.
    # The formatter function will be called whenever either state changes.
    switch_status.and_(combo_selection).bind_to(
        status_label,
        'text',
        lambda status, selection: f"Switch is {status}, Selection is {selection}"
    )
    
    # Handlers to update the state using the new objects
    def handle_switch_toggle(checked):
        switch_status.set("ON" if checked else "OFF")

    def handle_combo_change(new_text):
        combo_selection.set(new_text)

    return ui.Column(props={"spacing": 15, "margin": "20px"}, children=[
        ui.Label("New Widget Demo", props={"font-size": "16px", "font-weight": "bold"}),
        ui.Row(props={"spacing": 10}, children=[
            ui.Switch("Toggle Me", on_toggle=handle_switch_toggle),
            ui.ComboBox(
                items=["Item 1", "Item 2", "Item 3"],
                on_change=handle_combo_change
            )
        ]),
        status_label
    ])

def create_traits_demo_tab():
    """This component demonstrates the new trait system."""

    # -- Hover Effect Trait Demo --
    # First, let's add a global style rule that targets our new dynamic property.
    # Any widget with the property 'hover="true"' will get this style.
    winup.style.add_style_dict({
        '[hover="true"]': {
            "background-color": "#E8F5E9", # A light green
            "border": "1px solid #4CAF50",
        },
        ".highlighted": {
            "background-color": "#FFF9C4", # A light yellow
            "color": "black", # Ensure text is readable
        }
    })

    hover_label = ui.Label("Hover over me for a style change!")
    # Now, we just add the trait. The styling is handled automatically.
    traits.add_trait(hover_label, "hover_effect")
    # We can still have a tooltip as well! Traits are composable.
    traits.add_trait(hover_label, "tooltip", text="The style change comes from the HoverEffectTrait!")


    # -- Context Menu Demo --
    def on_hello(): print("Context Menu: Hello!")
    def on_world(): print("Context Menu: World!")

    context_menu_frame = ui.Frame(props={"background-color": "#EEEEEE", "min-height": "50px"})
    context_menu_frame.set_layout(ui.VBox(props={"alignment": "AlignCenter"}))
    context_menu_frame.add_child(ui.Label("Right-click me!"))
    traits.add_trait(context_menu_frame, "context_menu", items={
        "Say Hello": on_hello,
        "Say World": on_world,
    })

    # -- Draggable Demo --
    draggable_frame = ui.Frame(props={"background-color": "#D6EAF8", "min-height": "50px", "min-width": "150px"})
    draggable_frame.set_layout(ui.VBox(props={"alignment": "AlignCenter"}))
    draggable_frame.add_child(ui.Label("Drag me!"))
    traits.add_trait(draggable_frame, "draggable")
    highlight_label = ui.Label("You can select and copy this text.")
    traits.add_trait(highlight_label, "highlightable")

    return ui.Column(props={"spacing": 15, "margin": "20px"}, children=[
        ui.Label("Trait System Demo", props={"font-size": "16px", "font-weight": "bold"}),
        hover_label,
        highlight_label, # <-- Add the new label here
        context_menu_frame,
        draggable_frame
    ])

def create_id_demo_tab():
    """This component demonstrates using the 'id' prop for styling."""
    
    # Add a style rule specifically targeting the ID '#special-label'
    winup.style.add_style_dict({
        "#special-label": {
            "background-color": "#FFDDC1",
            "border": "2px dashed #FF5722",
            "padding": "10px",
            "font-weight": "bold",
        }
    })
    
    return ui.Column(props={"spacing": 15, "margin": "20px"}, children=[
        ui.Label("ID Prop Styling Demo", props={"font-size": "16px", "font-weight": "bold"}),
        ui.Label(
            "This label is styled with an ID selector.",
            props={"id": "special-label"}
        )
    ])

# --- 2. Define the Main Application Component ---

def App():
    """The main app uses a TabView to organize the demos."""
    
    # Create the content for each tab
    widgets_tab = create_widgets_demo_tab()
    traits_tab = create_traits_demo_tab()
    id_tab = create_id_demo_tab()

    return ui.TabView(tabs={
        "New Widgets": widgets_tab,
        "Traits Demo": traits_tab,
        "ID Demo": id_tab,
    })

# --- 3. Run the App ---

if __name__ == "__main__":
    winup.run(
        main_component_path="new_features_test:App",
        title="New Widgets & Traits Demo",
        width=450,
        height=300
    ) 