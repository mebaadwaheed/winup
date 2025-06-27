# Notifications Tool

The `winup.tools.notifications` module provides a simple way to send native system notifications.

*   `send(title, message, urgency)`: Sends a notification.
    *   `urgency` can be 'low', 'normal', or 'critical' (primarily for Linux).
    *   On Windows, this will appear as a standard message box.

```python
import winup
from winup import ui
from winup.tools import notifications

def App():
    def on_click():
        notifications.send(
            title="Hello from WinUp!",
            message="This is a native system notification.",
            urgency="normal"
        )

    return ui.Button("Send Notification", on_click=on_click)

# Example: winup.run(main_component_path="notify_demo:App", title="Notification Demo")
```