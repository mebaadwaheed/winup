from .core.window import _winup_app, Window
from .core.component import component
from .core.events import event_bus as events
from .core.hot_reload import hot_reload_service, _import_from_string
from .core.memoize import memo, clear_memo_cache
from typing import Optional

from . import ui
from . import style
from .state import state
from .tools import wintools, profiler
from . import shell
from . import tasks
from . import traits
from . import net

import sys
import importlib
from PySide6.QtCore import QTimer

# --- Main API ---

def run(main_component_path: str, title="WinUp App", width=800, height=600, icon=None, dev=False, menu_bar: Optional[shell.MenuBar] = None, tool_bar: Optional[shell.ToolBar] = None, status_bar: Optional[shell.StatusBar] = None, tray_icon: Optional[shell.SystemTrayIcon] = None):
    """
    The main entry point for a WinUp application.
    ... (docstring) ...
    Args:
        ...
        dev (bool): If True, enables development features like hot reloading.
        # --- ADD THESE ARGS TO DOCSTRING ---
        menu_bar (shell.MenuBar): A MenuBar object for the main window.
        tool_bar (shell.ToolBar): A ToolBar object for the main window.
        status_bar (shell.StatusBar): A StatusBar object for the main window.
        tray_icon (shell.SystemTrayIcon): An icon for the system tray.
    """
    # Initialize the style manager immediately, before any widgets are created.
    style.init_app(_winup_app.app)

    main_component = _import_from_string(main_component_path)
    main_widget = main_component()
    
    # --- ADD THIS ---
    shell_kwargs = {
        "menu_bar": menu_bar,
        "tool_bar": tool_bar,
        "status_bar": status_bar,
    }

    # Pass shell components to the main window factory
    main_window = _winup_app.create_main_window(main_widget, title, width, height, icon, **shell_kwargs)
    
    # Initialize all modules that require a window instance
    wintools.init_app(main_window)
    
    # --- NEW HOT RELOAD LOGIC ---
    # Enable hot reloading if in dev mode
    if dev:
        print("Development mode enabled. Starting hot reloader...")
        
        def on_reload():
            """
            Dynamically re-imports the main component and rebuilds the entire UI.
            """
            nonlocal main_component
            try:
                print("[Hot Reload] Reloading UI on main thread...")
                
                # Dynamically get the LATEST version of the component
                fresh_main_component = _import_from_string(main_component_path)
                
                print(f"[Hot Reload] Replacing old component: {main_component}")
                print(f"[Hot Reload] With new component: {fresh_main_component}")

                # Destroy the old widget to trigger unmount hooks
                old_widget = main_window.centralWidget()
                if old_widget:
                    old_widget.deleteLater()

                # Create the new UI
                new_widget = fresh_main_component()
                main_window.setCentralWidget(new_widget)
                
                # Update the reference for the next reload
                main_component = fresh_main_component
                
                print("[Hot Reload] UI Reloaded successfully.")
            except Exception as e:
                print(f"[Hot Reload] Error during component reload: {e}")
                import traceback
                traceback.print_exc()

        def schedule_reload():
            """
            This function is called by the hot reload service in the
            background thread. It schedules the actual reload on the
            main GUI thread.
            """
            QTimer.singleShot(0, on_reload)

        hot_reload_service.start(callback=schedule_reload)

    # Run the application event loop
    _winup_app.run()


__all__ = [
    "run", "Window", "hot_reload_service", "events", 
    "ui", "style", "state", "tools", "profiler",
    "component", "memo", "clear_memo_cache",
    "shell", "tasks", "traits", "net"
]
