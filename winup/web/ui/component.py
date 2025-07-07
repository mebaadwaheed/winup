from typing import List, Dict, Any, Optional, Callable
import uuid
from ..script_manager import script_manager
from ..py_to_js import transpile_hook
from ..event_manager import event_manager

class Component:
    def __init__(self, children: Optional[List['Component']] = None, props: Optional[Dict[str, Any]] = None):
        self.children = children or []
        self.props = props or {}

        # --- Handle State Binding ---
        # `bind_text` for one-way binding to textContent
        bind_text_key = self.props.pop('bind_text', None)
        if bind_text_key:
            self.props['data-bind-text'] = bind_text_key
            # Set the initial text from the state for the first render
            from winup.web.state import state
            if 'text' not in self.props:
                self.props['text'] = state.get(bind_text_key)

        # `bind_value` for two-way binding on inputs/textareas
        bind_value_key = self.props.pop('bind_value', None)
        if bind_value_key:
            self.props['data-bind-value'] = bind_value_key
            from winup.web.state import state
            # Set the initial value from the state
            self.props['value'] = state.get(bind_value_key)

        # `bind_checked` for two-way binding to a checkbox's checked status
        bind_checked_key = self.props.pop('bind_checked', None)
        if bind_checked_key:
            self.props['data-bind-checked'] = bind_checked_key
            from winup.web.state import state
            # Set the initial checked status from the state
            self.props['checked'] = state.get(bind_checked_key)

        # Allow user-defined IDs, otherwise generate one.
        if 'id' in self.props:
            self.component_id = self.props['id']
        else:
            self.component_id = f"winup-c-{uuid.uuid4().hex}"
            self.props['id'] = self.component_id

        # --- Handle lifecycle hooks ---
        self._process_lifecycle_hook('on_mount')
        self._process_lifecycle_hook('on_unmount')
        
        # --- Handle event handlers ---
        self._process_event_handlers()

    def _process_event_handlers(self):
        """
        Processes event handler props (on_click, etc.), registering Python
        callables with the event manager to be triggered from the client.
        """
        for prop_name in list(self.props.keys()):
            js_event_name = prop_name.replace('_', '').lower()
            
            if js_event_name.startswith('on'):
                handler = self.props.pop(prop_name)
                
                if isinstance(handler, Callable):
                    # Register the Python function and get a unique ID
                    event_id = event_manager.register_handler(handler)
                    # The JS call will send the event ID back to the server
                    self.props[js_event_name] = f"winup.sendEvent('{event_id}', event)"
                elif isinstance(handler, str):
                    # Raw JS strings are still supported for client-only logic
                    self.props[js_event_name] = handler

    def _process_lifecycle_hook(self, hook_name: str):
        """
        Processes a lifecycle hook, transpiling it from Python to JS if necessary.
        The hook is expected to take one argument: the component's HTML element.
        """
        handler = self.props.pop(hook_name, None)
        if not handler:
            return

        script = ""
        if isinstance(handler, str):
            # Handler is already a JS string
            script = handler
        elif isinstance(handler, Callable):
            # Transpile the Python function to JS
            # The hook function will be called in JS with the element as the first argument.
            is_async, js_body = transpile_hook(handler, js_args=['element'])
            if is_async:
                script = f"(async (element) => {{ {js_body} }})(this)"
            else:
                script = f"((element) => {{ {js_body} }})(this)"
        
        if script:
            if hook_name == 'on_mount':
                script_manager.add_mount_script(self.component_id, script)
            elif hook_name == 'on_unmount':
                script_manager.add_unmount_script(self.component_id, script)

    def render(self) -> str:
        raise NotImplementedError("Each component must implement a render method.")

    def __str__(self):
        return self.render() 