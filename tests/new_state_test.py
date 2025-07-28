import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, state

def NewStateApp():
    """A component demonstrating the new state management features."""

    # 1. Create state objects using the new API
    counter = state.create("counter", 0)
    step = state.create("step", 1)

    # 2. Create UI widgets
    # This label will be bound to both 'counter' and 'step'
    main_label = ui.Label()

    # This label will be bound to only the 'counter' with a simple format
    counter_mirror_label = ui.Label()
    
    # 3. Create bindings using the new flexible `bind_to` method

    # Bind to multiple states with a complex format
    counter.and_(step).bind_to(
        main_label, 
        'text', 
        lambda c, s: f"Counter is {c} (increment by {s})"
    )

    # Bind to a single state
    counter.bind_to(
        counter_mirror_label,
        'text',
        lambda c: f"The counter value is currently: {c}"
    )

    # 4. Define actions to modify the state
    def increment():
        counter.set(counter.get() + step.get())

    def change_step():
        # Cycle through step values 1, 2, 3
        current_step = step.get()
        new_step = (current_step % 3) + 1
        step.set(new_step)
        
    def reset():
        counter.set(0)
        step.set(1)

    # 5. Arrange widgets in a layout
    return ui.Column(props={"spacing": 15, "margin": "20px"}, children=[
        main_label,
        counter_mirror_label,
        ui.Row(props={"spacing": 10}, children=[
            ui.Button("Increment", on_click=increment),
            ui.Button("Change Step", on_click=change_step),
            ui.Button("Reset", on_click=reset),
        ])
    ])


if __name__ == "__main__":
    winup.run(
        main_component_path="new_state_test:NewStateApp",
        title="New State Management Demo",
        width=600,
        height=300
    ) 