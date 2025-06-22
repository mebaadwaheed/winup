import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import winup
from winup import ui
from winup.tools import notifications

def App():
    """
    A test application to showcase the new Slider and Notification features.
    """

    # 1. --- Create a label to display the slider's value ---
    value_label = ui.Label("Current Value: 50", props={"font-size": "16px"})

    # 2. --- Define a function to handle slider value changes ---
    def handle_slider_change(new_value):
        value_label.set_text(f"Current Value: {new_value}")

    # 3. --- Define a function to send a notification ---
    def send_notification():
        try:
            current_value = slider.get_value()
            notifications.send(
                title="Slider Notification",
                message=f"The slider's current value is {current_value}.",
                urgency="normal"
            )
            print("Notification sent successfully.")
        except Exception as e:
            print(f"Failed to send notification: {e}")

    # 4. --- Create the custom slider ---
    # Here we test all the new parameters
    slider = ui.Slider(
        min=0,
        max=100,
        step=5,
        value=50,
        on_change=handle_slider_change,
        track_color="#4a90e2",  # A nice blue color for the track
        thumb_style={
            "background-color": "#f5a623", # An orange thumb
            "border": "2px solid #d08c1d"
        }
    )

    # 5. --- Create the button to trigger the notification ---
    notify_button = ui.Button("Send Notification", on_click=send_notification)

    # 6. --- Arrange the widgets in a layout ---
    return ui.Column(
        children=[
            ui.Label("Custom Slider and Notification Test", props={"font-size": "20px", "font-weight": "bold"}),
            value_label,
            slider,
            notify_button
        ],
        props={
            "spacing": 15,
            "alignment": "center",
            "padding": "20px"
        }
    )

if __name__ == "__main__":
    winup.run(main_component_path="slider_notification_test:App", title="Slider & Notification Test") 