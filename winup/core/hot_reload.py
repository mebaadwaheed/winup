"""
The WinUp Hot Reloading System.

This module provides the core logic for automatically reloading the UI
when source code files change.
"""
import sys
import importlib
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from PySide6.QtCore import QObject, Signal

def _import_from_string(import_str: str):
    """
    Dynamically imports an attribute from a module given a string path.
    e.g., "my_app.components:MyComponent"
    """
    module_str, _, attr_str = import_str.rpartition(':')
    if not module_str or not attr_str:
        raise ImportError(f"Invalid import string '{import_str}'. Must be in 'module.path:attribute' format.")
    
    try:
        print(f"[Hot Reload] Importing '{attr_str}' from '{module_str}'")
        module = importlib.import_module(module_str)
        # The module might have been reloaded, so we need to get the fresh object.
        importlib.reload(module)
        return getattr(module, attr_str)
    except ImportError as e:
        print(f"[Hot Reload] Error importing module '{module_str}': {e}")
        raise
    except AttributeError:
        print(f"[Hot Reload] Error: Attribute '{attr_str}' not found in module '{module_str}'.")
        raise


# --- NEW: Signal Emitter for Cross-Thread Communication ---
class _ReloadSignalEmitter(QObject):
    """An object to safely emit signals from a background thread to the main GUI thread."""
    reload_requested = Signal()


# --- The main Hot Reload Service ---

class _HotReloadService:
    """A singleton service that manages file watching and UI reloading."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_HotReloadService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Prevent re-initialization
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.observer = Observer()
        self.signal_emitter = _ReloadSignalEmitter()
        self._watched_files = set()
        self._initialized = True
        print("Hot Reload Service initialized.")
    
    def start(self, callback: callable):
        """
        Starts watching all non-site-package modules for changes.

        Args:
            callback: The function to call on the main thread when a file is changed.
        """
        # Connect the signal from the background thread to the main thread's callback
        self.signal_emitter.reload_requested.connect(callback)
        
        project_paths = self._get_project_module_paths()
        
        event_handler = _ChangeHandler(self._on_file_changed)

        for path in project_paths:
            # Watch the directory of each project file
            dir_path = os.path.dirname(path)
            if dir_path and os.path.isdir(dir_path) and dir_path not in self._watched_files:
                self.observer.schedule(event_handler, dir_path, recursive=False)
                self._watched_files.add(dir_path)
        
        if not self.observer.is_alive():
            self.observer.start()

    def _get_project_module_paths(self) -> set:
        """
        Inspects sys.modules to find all file paths that are part of the
        current project (i.e., not in site-packages).
        """
        paths = set()
        site_packages_path = os.path.normpath(sys.prefix)

        for module_name, module in sys.modules.items():
            if hasattr(module, '__file__') and module.__file__:
                module_path = os.path.normpath(module.__file__)
                # Ignore files in the standard library and site-packages
                if site_packages_path not in module_path:
                    # Also ignore the framework's own files to prevent cycles
                    if 'winup' not in module_path:
                        paths.add(module_path)
        return paths

    def _on_file_changed(self, file_path: str):
        """
        Handles the file change event. Invalidates the import cache for the
        changed module and triggers the reload signal.
        """
        if not file_path.endswith('.py'):
            return

        print(f"Detected change in: {file_path}. Requesting reload...")
        
        # --- NEW: More robust module finding ---
        module_to_reload = None
        # Normalize the path for reliable comparison, and convert to lowercase
        normalized_path = os.path.normpath(file_path).lower()

        for module in sys.modules.values():
            if hasattr(module, '__file__') and module.__file__:
                # Compare lowercase paths to handle case-insensitivity on Windows
                if os.path.normpath(module.__file__).lower() == normalized_path:
                    module_to_reload = module
                    break
        
        if module_to_reload:
            try:
                # The '__main__' module cannot be reloaded, but we still want to
                # trigger the UI refresh to pick up changes.
                if module_to_reload.__name__ == '__main__':
                    print(f"[Hot Reload] Change detected in __main__ module. Triggering UI refresh without reload.")
                else:
                    print(f"[Hot Reload] Reloading module: {module_to_reload.__name__}")
                    importlib.reload(module_to_reload)
                
                # Emit signal to trigger callback on the main thread
                self.signal_emitter.reload_requested.emit()

            except Exception:
                print(f"[Hot Reload] Error reloading module.")
                traceback.print_exc()
        else:
            print(f"Warning: Could not find module for path {file_path}")

# --- Watchdog Event Handler ---

class _ChangeHandler(FileSystemEventHandler):
    """A simple handler that calls a callback on any file modification."""
    def __init__(self, on_change_callback):
        self._on_change = on_change_callback

    def on_modified(self, event):
        if not event.is_directory:
            self._on_change(event.src_path)

# --- Public API ---

# Singleton instance of the service
hot_reload_service = _HotReloadService()