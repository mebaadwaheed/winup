from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional, List

class ScrollView(Component):
    """A container that provides scrolling for its content."""
    
    def __init__(self, children: Optional[List[Component]] = None, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        
        default_style = {
            'overflow': 'auto',
            'height': '300px',
            'border': '1px solid #eee',
            'padding': '10px',
            'border_radius': '5px',
        }
        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style

        super().__init__(children=children, props=all_props)

    def render(self) -> str:
        """Renders the scrollable container and its children."""
        children_html = "".join(child.render() for child in self.children)
        return f"<div{props_to_html(self.props)}>{children_html}</div>" 