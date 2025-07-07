# winup/web/state.py
from __future__ import annotations
from typing import Any, Dict, List, Callable
import asyncio

class State:
    """A handle to a piece of state in the global state manager."""
    def __init__(self, key: str, manager: StateManager):
        self._key = key
        self._manager = manager

    def get(self) -> Any:
        """Gets the current value of the state."""
        return self._manager.get(self._key)

    async def set(self, value: Any):
        """Sets the new value of the state and broadcasts it."""
        await self._manager.set(self._key, value)


class StateManager:
    """Manages the application's global state and WebSocket connections."""
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._connections: List[Any] = [] # List of active WebSockets

    def get(self, key: str) -> Any:
        """Gets a value from the state dictionary."""
        return self._state.get(key)

    async def set(self, key: str, value: Any):
        """Sets a value in the state and broadcasts it to all clients."""
        self._state[key] = value
        await self.broadcast(key, value)

    def create(self, key: str, initial_value: Any = None) -> State:
        """Creates a new state variable and returns a handle to it."""
        if key not in self._state:
            self._state[key] = initial_value
        return State(key, self)

    def add_connection(self, websocket: Any):
        """Adds a new client WebSocket connection."""
        self._connections.append(websocket)

    def remove_connection(self, websocket: Any):
        """Removes a client WebSocket connection."""
        self._connections.remove(websocket)

    async def broadcast(self, key: str, value: Any):
        """Sends a state update to all connected clients."""
        message = {"type": "state_update", "key": key, "value": value}
        # Use asyncio.gather to send all messages concurrently
        await asyncio.gather(
            *[conn.send_json(message) for conn in self._connections]
        )

# Global singleton instance of the state manager
state = StateManager() 