from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional

class Button(Component):
    """A clickable button component."""

    def __init__(self, text: str = "", props: Optional[Dict[str, Any]] = None, **kwargs):
        # Define default styles for a modern look
        default_style = {
            'background_color': '#007bff',
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'text_align': 'center',
            'text_decoration': 'none',
            'display': 'inline-block',
            'font_size': '16px',
            'margin': '4px 2px',
            'cursor': 'pointer',
            'border_radius': '5px',
            'transition': 'background-color 0.3s',
        }
        
        # Merge kwargs and props, with user's props taking precedence
        all_props = (props or {}) | kwargs
        
        # Merge styles, with user's styles taking precedence
        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style

        super().__init__(props=all_props)
        self.text = text

    def render(self) -> str:
        """Renders the button as an HTML <button> element."""
        all_props = self.props.copy()
        text_content = all_props.pop('text', self.text)
        
        return f"<button{props_to_html(all_props)}>{text_content}</button>" 