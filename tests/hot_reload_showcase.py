import winup
from winup import ui

# The main component for the application.
@winup.component
def App():
    """
    A simple component that displays a label.
    Try changing the text below, save the fle, and the UI should update instantly.
    """
    return ui.Label(
        "Hello, WinUp Hot Reload! It's working!",
        props={"font-size": "24px", "alignment": "AlignCenter"}
    )

# --- NEW: Main execution block ---
if __name__ == "__main__":
    # Add the project root to the Python path to allow for absolute imports
    # like 'tests.hot_reload_showcase:App'
    import sys
    import os
    # This assumes the script is run from the project root.
    # If not, you might need a more robust way to find the root.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Run the app using the new string-based path.
    # The format is 'path.to.module:ComponentName'
    winup.run(
        main_component_path="tests.hot_reload_showcase:App",
        title="Hot Reload Showcase",
        dev=True
    )