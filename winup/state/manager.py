from PySide6.QtWidgets import QWidget, QLineEdit, QCheckBox
from typing import TypeVar, Generic, Any, Callable, cast, Dict
import asyncio

T = TypeVar('T')

class State(Generic[T]):
    """A wrapper for a single piece of state, providing a typed interface."""
    def __init__(self, key: str, manager: 'StateManager', initial_value: T):
        self._key = key
        self._manager = manager
        # Set the initial value in the manager
        if key not in self._manager._state:
            self._manager._state[key] = initial_value

    def get(self) -> T:
        """Gets the current value of the state."""
        return cast(T, self._manager.get(self._key))

    def set(self, value: T):
        """Sets a new value for the state. (For Desktop)"""
        # This is a synchronous wrapper for desktop applications.
        # It calls the async set method but doesn't wait for it.
        self._manager.set_sync(self._key, value)


    async def set_async(self, value: T):
        """Sets a new value for the state and broadcasts to web clients if applicable."""
        await self._manager.set(self._key, value)

    def subscribe(self, callback: Callable):
        """Subscribes a callback to changes in this state."""
        self._manager.subscribe(self._key, callback)

    def bind_to(self, widget: QWidget, property_name: str, formatter: Callable):
        """Binds this state to a widget's property using a formatter."""
        # Use a MultiStateBinding with a single state for consistency
        MultiStateBinding(self._manager, self).bind_to(widget, property_name, formatter)

    def and_(self, *others: 'State') -> 'MultiStateBinding':
        """Combines this state with others to create a multi-state binding."""
        return MultiStateBinding(self._manager, self, *others)

class MultiStateBinding:
    """Represents a binding to multiple state objects."""
    def __init__(self, manager: 'StateManager', *states: State):
        self._manager = manager
        self._states = states
        self._keys = [s._key for s in states]

    def bind_to(self, widget: QWidget, property_name: str, formatter: Callable):
        """
        Binds the collected states to a widget's property using a formatter.
        """
        self._manager.bind_to(self._keys, widget, property_name, formatter)

class StateManager:
    """A centralized state management system for WinUp applications."""

    def __init__(self):
        self._state = {}
        # Stores bindings: {'state_key': [(widget, 'property_name'), ...]}
        self._bindings = {}
        # Stores subscriptions: {'state_key': [callback1, callback2, ...]}
        self._subscriptions = {}
        # Stores complex bindings: {'state_key': [binding_info, ...]}
        self._complex_bindings = {}
        # Holds created State objects to ensure singletons per key
        self._state_objects = {}
        # For web context
        self._is_web_context = False
        self._web_connections: list[Any] = []


    def set_web_context(self, is_web: bool):
        """Sets the state manager to operate in a web context."""
        self._is_web_context = is_web

    def add_web_connection(self, websocket: Any):
        """Adds a new client WebSocket connection."""
        self._web_connections.append(websocket)

    def remove_web_connection(self, websocket: Any):
        """Removes a client WebSocket connection."""
        self._web_connections.remove(websocket)

    async def broadcast(self, key: str, value: Any):
        """Sends a state update to all connected web clients."""
        if not self._is_web_context:
            return
        message = {"type": "state_update", "key": key, "value": value}
        # Use asyncio.gather to send all messages concurrently
        await asyncio.gather(
            *[conn.send_json(message) for conn in self._web_connections]
        )


    def create(self, key: str, initial_value=None) -> State:
        """
        Creates or retrieves a managed State object.
        This is the new recommended way to handle state.
        """
        if key not in self._state_objects:
            self._state_objects[key] = State(key, self, initial_value)
        else:
            # If state already exists, make sure its value is not reset
            pass
        return self._state_objects[key]

    def set_sync(self, key: str, value):
        """
        Synchronously sets a value and updates desktop components.
        """
        if self._state.get(key) == value:
            return  # No change, no update needed

        self._state[key] = value

        # --- Synchronous updates for Desktop ---
        self._update_bindings(key)
        self._update_complex_bindings(key)
        self._execute_subscriptions(key)

    async def set(self, key: str, value, sync_only=False):
        """
        Sets a value in the state and updates all bound widgets and subscriptions.
        If in web context, it also broadcasts the change to clients.
        """
        if self._state.get(key) == value:
            return # No change, no update needed

        self._state[key] = value

        # --- Synchronous updates for Desktop ---
        self._update_bindings(key)
        self._update_complex_bindings(key)
        self._execute_subscriptions(key)

        # --- Asynchronous broadcast for Web ---
        if self._is_web_context and not sync_only:
            await self.broadcast(key, value)
            


    def get(self, key: str, default=None):
        """Gets a value from the state."""
        return self._state.get(key, default)

    def subscribe(self, key: str, callback: Callable):
        """
        Subscribes a callback function to a state key. The callback will be
        executed whenever the state value changes.

        The callback will be immediately called with the current value upon subscription.
        """
        if key not in self._subscriptions:
            self._subscriptions[key] = []
        self._subscriptions[key].append(callback)
        # Immediately call with current value
        callback(self.get(key))

    def bind_to(self, state_keys: list[str], widget: QWidget, property_name: str, formatter: Callable):
        """
        Binds one or more state keys to a widget's property using a formatter function.

        Args:
            state_keys: A list of state keys to depend on.
            widget: The target widget.
            property_name: The name of the property to update (e.g., 'text').
            formatter: A function that takes the state values as arguments (in order)
                       and returns the formatted value for the property.
        """
        binding_info = {
            "keys": state_keys,
            "widget": widget,
            "property": property_name,
            "formatter": formatter,
        }

        # Register this binding for each key it depends on
        for key in state_keys:
            if key not in self._complex_bindings:
                self._complex_bindings[key] = []
            self._complex_bindings[key].append(binding_info)

        # Immediately apply the binding
        self._apply_complex_binding(binding_info)

    def bind_two_way(self, widget: QWidget, state_key: str):
        """
        Creates a two-way data binding between a widget and a state key.
        The widget will update the state, and the state will update the widget.
        """
        # Determine the property and signal based on widget type
        if isinstance(widget, QLineEdit):
            prop_name = "text"
            signal = widget.textChanged
        elif isinstance(widget, QCheckBox):
            prop_name = "checked"
            signal = widget.stateChanged
        else:
            raise TypeError(f"Widget type '{type(widget).__name__}' does not support two-way binding.")

        # 1. State -> Widget binding (like the normal bind)
        self.bind(widget, prop_name, state_key)
        
        # 2. Widget -> State binding
        # When the widget's signal is emitted, update the state
        signal.connect(lambda value: self.set(state_key, value))

    def bind(self, widget: QWidget, property_name: str, state_key: str):
        """
        Binds a widget's property to a key in the state.

        When the state key is updated via `set()`, the widget's property
        will be automatically updated with the new value.

        Args:
            widget: The UI widget to bind (e.g., a Label, Input).
            property_name: The name of the widget's property to update (e.g., 'text', 'checked').
            state_key: The key in the state store to bind to.
        """
        # Set the initial value on the widget
        initial_value = self.get(state_key)
        if initial_value is not None:
            self._set_widget_property(widget, property_name, initial_value)
        
        # Register the binding for future updates
        if state_key not in self._bindings:
            self._bindings[state_key] = []
        self._bindings[state_key].append((widget, property_name))

    def _update_bindings(self, key: str):
        """Update all widgets bound to a specific state key."""
        if key not in self._bindings:
            return

        new_value = self.get(key)
        for widget, property_name in self._bindings[key]:
            self._set_widget_property(widget, property_name, new_value)
            
            # Repolish to apply any style changes if needed
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def _execute_subscriptions(self, key: str):
        """Execute all callbacks subscribed to a specific state key."""
        if key in self._subscriptions:
            new_value = self.get(key)
            for callback in self._subscriptions[key]:
                callback(new_value)

    def _set_widget_property(self, widget, property_name, value):
        """Helper to set a property on a widget, trying setter method first."""
        # Special handling for the 'style' property
        if property_name == 'style' and isinstance(value, dict):
            from winup.style.styler import styler
            styler.apply_props(widget, value)
            return

        setter = getattr(widget, f"set{property_name.capitalize()}", None)
        try:
            if setter and callable(setter):
                setter(value)
            else:
                widget.setProperty(property_name, value)
        except RuntimeError:
            # This can happen if the widget is deleted while a state change is in flight.
            # It's safe to ignore, as the widget is gone anyway.
            return
        
        # Repolish the widget to apply any potential style changes
        try:
            if widget and widget.style():
                widget.style().unpolish(widget)
                widget.style().polish(widget)
        except RuntimeError:
            pass # Widget was deleted, do nothing.

    def _update_complex_bindings(self, updated_key: str):
        """Update all complex bindings that depend on the updated key."""
        if updated_key not in self._complex_bindings:
            return

        # Use a set to avoid updating the same binding multiple times if it depends on several updated keys
        bindings_to_update = set()
        for binding_info in self._complex_bindings[updated_key]:
            # Create a tuple of the binding's components to make it hashable for the set
            bindings_to_update.add(
                (
                    tuple(binding_info["keys"]),
                    binding_info["widget"],
                    binding_info["property"],
                    binding_info["formatter"],
                )
            )

        for keys, widget, prop, formatter in bindings_to_update:
            binding_info = {
                "keys": list(keys),
                "widget": widget,
                "property": prop,
                "formatter": formatter,
            }
            self._apply_complex_binding(binding_info)

    def _apply_complex_binding(self, binding_info: dict):
        """Gathers current state values and applies a complex binding's formatter."""
        # Gather the current values for all keys the binding depends on
        values = [self.get(k) for k in binding_info["keys"]]

        # Call the formatter with the values
        try:
            formatted_value = binding_info["formatter"](*values)
            # Update the widget property
            self._set_widget_property(
                binding_info["widget"], binding_info["property"], formatted_value
            )
        except Exception as e:
            print(f"Error applying binding: {e}")

