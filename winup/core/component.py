import functools
import inspect
from typing import Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout

class Component(QWidget):
    """A base class for all WinUp components, handling lifecycle events."""
    
    def __init__(self, render_func: Callable, props: dict, on_mount: Callable = None, on_unmount: Callable = None):
        super().__init__()
        self.render_func = render_func
        self.props = props
        self.on_mount_handler = on_mount
        self.on_unmount_handler = on_unmount
        self.child_component = None # The actual rendered widget from the user's function
        
        # Set the object name if 'id' is provided in props, for CSS styling
        if "id" in self.props:
            self.setObjectName(str(self.props["id"]))

        # Every component gets a default layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Initial render
        self.render()

    def render(self):
        """Calls the user's render function and adds the result to the layout."""
        # Clear previous content if any
        if self.layout().count() > 0:
            while (item := self.layout().takeAt(0)) is not None:
                if item.widget():
                    # If the child is a Component, call its unmount handler
                    if isinstance(item.widget(), Component):
                        item.widget()._unmount()
                    item.widget().deleteLater()

        # Call the user's component function to get the new widget
        self.child_component = self.render_func(**self.props)
        if not isinstance(self.child_component, QWidget):
            raise TypeError(
                f"Component '{self.render_func.__name__}' must return a QWidget, "
                f"but it returned type '{type(self.child_component).__name__}'."
            )
        
        # After rendering, check if the child widget has lifecycle hooks attached to it.
        # This is the new mechanism to avoid passing them to Qt constructors.
        if hasattr(self.child_component, '_winup_on_mount'):
            self.on_mount_handler = self.child_component._winup_on_mount
        
        if hasattr(self.child_component, '_winup_on_unmount'):
            self.on_unmount_handler = self.child_component._winup_on_unmount

        self.layout().addWidget(self.child_component)

    def showEvent(self, event):
        """Override the Qt showEvent to trigger the on_mount handler."""
        super().showEvent(event)
        if self.on_mount_handler:
            self.on_mount_handler()
            self.on_mount_handler = None # Only call once

    def closeEvent(self, event):
        """Override the Qt closeEvent to trigger the on_unmount handler."""
        self._unmount()
        # Also ensure child components are unmounted
        if isinstance(self.child_component, Component):
            self.child_component._unmount()
        super().closeEvent(event)

    def _unmount(self):
        """Internal method to trigger the on_unmount handler."""
        if self.on_unmount_handler:
            self.on_unmount_handler()

def component(func):
    """
    A decorator that turns a function into a Component class factory.
    It now supports on_mount and on_unmount lifecycle hooks.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # We no longer need to extract hooks here, as they are passed to child widgets.
        
        # The user's function now doesn't need to accept args, just kwargs (props)
        # We bind the args to the function signature to create the props dict
        sig = inspect.signature(func)
        try:
            bound_args = sig.bind(*args, **kwargs)
        except TypeError as e:
            # Provide a more helpful error message
            raise TypeError(f"Error calling component '{func.__name__}': {e}. Check the arguments being passed.")
            
        bound_args.apply_defaults()
        props = dict(bound_args.arguments)

        # The render function to be passed to the Component class
        def render_function(**p):
            return func(**p)
            
        # The lifecycle hooks are now picked up from the returned widget inside Component.render
        return Component(render_function, props)

    # Attach the original function's signature to the wrapper.
    # This helps avoid recursion issues with `inspect.signature` on decorated functions.
    wrapper.__signature__ = inspect.signature(func)
    return wrapper 