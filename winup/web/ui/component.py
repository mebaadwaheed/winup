from typing import List, Dict, Any, Optional, Callable
import uuid
from ..script_manager import script_manager
from ..py_to_js import transpile_hook
from ..event_manager import event_manager
from ...state import state
from ...style.tailwind import transpile_tailwind

class Component:
    def __init__(self, children: Optional[List['Component']] = None, props: Optional[Dict[str, Any]] = None):
        self.children = children or []
        self.props = props or {}

        # --- Handle Tailwind styling ---
        tailwind_string = self.props.pop('tailwind', None)
        if tailwind_string:
            # Transpile tailwind classes to a style dictionary
            tailwind_styles = transpile_tailwind(tailwind_string, platform='web')
            
            # Convert the style dictionary to a CSS string
            tailwind_css = "; ".join([f"{key}: {value}" for key, value in tailwind_styles.items()])
            
            # Merge with existing styles
            existing_style = self.props.get('style', '')
            if existing_style and not existing_style.strip().endswith(';'):
                existing_style += ';'
            
            self.props['style'] = f"{existing_style} {tailwind_css}".strip()

        # --- Handle State Binding ---
        # `bind_text` for one-way binding to textContent
        bind_text_key = self.props.pop('bind_text', None)
        if bind_text_key:
            self.props['data-bind-text'] = bind_text_key
            # Set the initial text from the state for the first render
            if 'text' not in self.props:
                self.props['text'] = state.get(bind_text_key)

        # `bind_value` for two-way binding on inputs/textareas
        bind_value_key = self.props.pop('bind_value', None)
        if bind_value_key:
            self.props['data-bind-value'] = bind_value_key
            # Set the initial value from the state
            self.props['value'] = state.get(bind_value_key)

        # `bind_checked` for two-way binding to a checkbox's checked status
        bind_checked_key = self.props.pop('bind_checked', None)
        if bind_checked_key:
            self.props['data-bind-checked'] = bind_checked_key
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

def component_to_html(qt_widget):
    """Convert a Qt widget to HTML representation for web rendering."""
    from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
    
    if hasattr(qt_widget, 'layout') and qt_widget.layout():
        layout = qt_widget.layout()
        html_parts = []
        
        # Handle different layout types
        if isinstance(layout, (QVBoxLayout, QHBoxLayout)):
            container_tag = "div"
            
            # Build CSS classes and styles
            css_classes = []
            inline_styles = []
            
            # Layout direction
            if isinstance(layout, QVBoxLayout):
                css_classes.append("flex flex-col")
            else:
                css_classes.append("flex flex-row")
            
            # Extract props from the widget if available
            widget_props = getattr(qt_widget, 'props', {}) or {}
            
            # Handle alignment
            alignment = widget_props.get('alignment', '')
            if 'AlignCenter' in alignment or 'center' in alignment.lower():
                css_classes.append("items-center justify-center")
                inline_styles.append("text-align: center")
            elif 'AlignLeft' in alignment or 'left' in alignment.lower():
                css_classes.append("items-start justify-start")
            elif 'AlignRight' in alignment or 'right' in alignment.lower():
                css_classes.append("items-end justify-end")
            
            # Handle spacing
            spacing = widget_props.get('spacing', layout.spacing())
            if spacing and spacing > 0:
                css_classes.append(f"gap-{min(spacing // 4, 12)}")  # Convert to Tailwind gap classes
            
            # Handle padding
            padding = widget_props.get('padding', '')
            if padding:
                inline_styles.append(f"padding: {padding}")
            
            # Handle other CSS properties
            for prop, value in widget_props.items():
                if prop in ['background-color', 'color', 'border', 'border-radius', 'margin', 'width', 'height']:
                    css_prop = prop.replace('_', '-')
                    inline_styles.append(f"{css_prop}: {value}")
            
            # Build the opening tag
            class_attr = f' class="{" ".join(css_classes)}"' if css_classes else ''
            style_attr = f' style="{"; ".join(inline_styles)}"' if inline_styles else ''
            
            html_parts.append(f'<{container_tag}{class_attr}{style_attr}>')
            
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    html_parts.append(widget_to_html(widget))
            
            html_parts.append(f'</{container_tag}>')
            
        return ''.join(html_parts)
    else:
        return widget_to_html(qt_widget)

def widget_to_html(widget):
    """Convert individual Qt widgets to HTML."""
    from PySide6.QtWidgets import QLabel, QPushButton
    
    # Extract props from widget if available
    widget_props = getattr(widget, 'props', {}) or {}
    
    # Build inline styles from props
    inline_styles = []
    for prop, value in widget_props.items():
        if prop in ['font-size', 'font-weight', 'color', 'background-color', 'padding', 'margin', 
                   'margin-top', 'margin-bottom', 'margin-left', 'margin-right', 'border', 
                   'border-radius', 'width', 'height', 'text-align']:
            css_prop = prop.replace('_', '-')
            inline_styles.append(f"{css_prop}: {value}")
    
    style_attr = f' style="{"; ".join(inline_styles)}"' if inline_styles else ''
    
    if isinstance(widget, QLabel):
        text = widget.text() or ""
        return f'<p{style_attr}>{text}</p>'
    elif isinstance(widget, QPushButton):
        text = widget.text() or "Button"
        # Combine default button styles with custom props
        default_classes = "px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        return f'<button class="{default_classes}"{style_attr}>{text}</button>'
    else:
        # Generic widget fallback
        class_name = widget.__class__.__name__
        return f'<div class="widget-{class_name.lower()}"{style_attr}>Widget: {class_name}</div>'