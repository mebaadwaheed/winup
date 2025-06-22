"""
A tool for sending system-level (OS) notifications.
Provides a simple, cross-platform API.
"""

import sys
import subprocess

def send(title: str, message: str, urgency: str = "normal"):
    """
    Sends a system notification.

    Args:
        title (str): The title of the notification.
        message (str): The body text of the notification.
        urgency (str): The urgency level (e.g., 'low', 'normal', 'critical').
                       This is primarily for Linux systems.
    
    Raises:
        OSError: If the notification command fails.
        NotImplementedError: If the OS is not supported.
    """
    platform = sys.platform

    try:
        if platform == "win32":
            # Windows: Uses a simple message box as a fallback for notifications.
            from winup.ui import dialogs
            dialogs.show_message(title, message, type="info")

        elif platform == "darwin":
            # macOS: Uses AppleScript.
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=True)

        elif platform.startswith("linux"):
            # Linux: Uses notify-send, which is common on most desktop environments.
            urgency_map = {"low": "low", "normal": "normal", "critical": "critical"}
            urgency_level = urgency_map.get(urgency.lower(), "normal")
            subprocess.run(["notify-send", f"--urgency={urgency_level}", title, message], check=True)

        else:
            raise NotImplementedError(f"System notifications are not supported on this platform: {platform}")

    except FileNotFoundError:
        # This occurs if the command (e.g., 'notify-send') is not found.
        print(f"Warning: Notification command not found. Could not send notification on platform '{platform}'.")
    except Exception as e:
        print(f"Error sending notification: {e}")
        raise OSError("Failed to send system notification.") from e 