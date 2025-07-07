# winup/web/event_manager.py
from typing import Dict, Callable, Any
import uuid

class EventManager:
    """
    A singleton class to manage and execute event handlers on the server
    that are triggered from the client.
    """
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}

    def register_handler(self, func: Callable) -> str:
        """
        Stores a Python function and returns a unique ID for it.
        """
        if not callable(func):
            return "" # Should not happen with current setup
        
        event_id = f"event-{uuid.uuid4().hex}"
        self._handlers[event_id] = func
        return event_id

    async def trigger_event(self, event_id: str, *args, **kwargs):
        """
        Finds and executes a registered event handler by its ID.
        """
        handler = self._handlers.get(event_id)
        if handler:
            # We can extend this to pass arguments from the client in the future
            return await handler(*args, **kwargs)
        else:
            print(f"Warning: Event handler with ID '{event_id}' not found.")

    def clear(self):
        """
        Clears all registered handlers. This can be useful for cleanup
        between server reloads in a development environment.
        """
        self._handlers.clear()

# Global singleton instance
event_manager = EventManager() 