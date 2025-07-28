import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, shell, tasks, profiler
import time

# --- 1. Define App Logic & Handlers ---

def handle_quit():
    print("Exit action triggered!")
    winup.core.window._winup_app.app.quit()

def show_about():
    about_text = "WinUp Framework\n\nA demo of professional app features."
    winup.ui.dialogs.show_message("About", about_text, type="info")

def task_finished(result):
    print(f"Background task finished with result: {result}")
    shell.StatusBar.show_message("Task complete!", 5000)

def task_error(error_details):
    e, trace = error_details
    print(f"An error occurred in the background task: {e}")
    shell.StatusBar.show_message(f"Error: {e}", 5000)

def task_started():
    shell.StatusBar.show_message("Running background task...")

# The function to be run in the background
@tasks.run(on_finish=task_finished, on_error=task_error, on_start=task_started)
def long_running_task(duration):
    print(f"Starting a long task for {duration} seconds...")
    time.sleep(duration)
    if duration > 3:
        raise ValueError("Duration is too long!")
    return f"Slept for {duration} seconds."

# --- 2. Define Shell Components ---

app_menu_bar = shell.MenuBar({
    "&File": {
        "&New": lambda: print("New file!"),
        "---": None,
        "&Quit": handle_quit
    },
    "&Help": {
        "&About": show_about
    }
})

app_tool_bar = shell.ToolBar({
    "Run Short Task": lambda: long_running_task(2),
    "Run Long Task (Error)": lambda: long_running_task(4)
})

app_status_bar = shell.StatusBar()

# Note: You'll need a real .png icon in your project root for this to work.
# app_tray_icon = shell.SystemTrayIcon(
#     icon_path="icon.png", 
#     tooltip="My Pro App",
#     menu_items={
#         "Show Message": lambda: shell.StatusBar.show_message("Hello from the tray!"),
#         "Quit": handle_quit
#     }
# )


# --- 3. Define Main UI Component ---

def App():
    return ui.Column(props={"alignment": "AlignCenter"}, children=[
        ui.Label("Professional App Shell Demo", props={"font-size": "24px"}),
        ui.Label("Check the Menu Bar, Tool Bar, and Status Bar."),
        ui.Row(props={"spacing": 10, "margin": "20px"}, children=[
            ui.Button("Run Short Task (2s)", on_click=lambda: long_running_task(2)),
            ui.Button("Run Long Task (4s, will fail)", on_click=lambda: long_running_task(4)),
        ])
    ])

# --- 4. Run the App ---

if __name__ == "__main__":
    winup.run(
        main_component_path="pro_app_test:App",
        title="Professional App Demo",
        width=700,
        height=400,
        menu_bar=app_menu_bar,
        tool_bar=app_tool_bar,
        status_bar=app_status_bar,
        # tray_icon=app_tray_icon, # Uncomment if you have an icon
    )
