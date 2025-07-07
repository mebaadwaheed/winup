from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional

class Link(Component):
    """A general-purpose hyperlink component."""

    def __init__(self, text: str = "", href: str = "#", props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        all_props['href'] = href
        
        default_style = {
            'color': '#007bff',
            'text_decoration': 'underline',
            'cursor': 'pointer',
        }
        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style

        super().__init__(props=all_props)
        self.text = text

    def render(self) -> str:
        """Renders the link as an HTML <a> element."""
        all_props = self.props.copy()
        text_content = all_props.pop('text', self.text)
        return f"<a{props_to_html(all_props)}>{text_content}</a>" 