from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional

class Input(Component):
    """A text input component."""

    def __init__(self, props: Optional[Dict[str, Any]] = None, **kwargs):
        default_style = {
            'font_size': '16px',
            'padding': '10px',
            'border': '1px solid #ccc',
            'border_radius': '5px',
            'box_sizing': 'border-box',
            'width': '100%',
        }
        all_props = (props or {}) | kwargs
        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style
        
        # Set default type if not provided
        if 'type' not in all_props:
            all_props['type'] = 'text'

        super().__init__(props=all_props)

    def render(self) -> str:
        """Renders the input as an HTML <input> element."""
        return f"<input{props_to_html(self.props)}>" 