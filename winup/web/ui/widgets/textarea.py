from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional

class TextArea(Component):
    """A multi-line text input component."""

    def __init__(self, value: str = "", props: Optional[Dict[str, Any]] = None, **kwargs):
        default_style = {
            'font_size': '16px',
            'padding': '10px',
            'border': '1px solid #ccc',
            'border_radius': '5px',
            'box_sizing': 'border-box',
            'width': '100%',
            'min_height': '100px',
            'font_family': 'sans-serif',
        }
        all_props = (props or {}) | kwargs
        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style

        super().__init__(props=all_props)
        self.value = value

    def render(self) -> str:
        """Renders the component as an HTML <textarea> element."""
        all_props = self.props.copy()
        value_content = all_props.pop('value', self.value)
        return f"<textarea{props_to_html(all_props)}>{value_content}</textarea>" 