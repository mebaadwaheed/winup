from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional, List

class Flex(Component):
    """A flexible layout component using CSS Flexbox."""

    def __init__(self, children: Optional[List[Component]] = None, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        
        default_style = {
            'display': 'flex',
            'flex-direction': all_props.pop('direction', 'row'),
            'justify-content': all_props.pop('justify_content', 'flex-start'),
            'align-items': all_props.pop('align_items', 'stretch'),
            'gap': all_props.pop('gap', '0px'),
            'flex-wrap': all_props.pop('wrap', 'nowrap'),
        }

        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style

        super().__init__(children=children, props=all_props)

    def render(self) -> str:
        """Renders the flex container and its children."""
        children_html = "".join(child.render() for child in self.children)
        return f"<div{props_to_html(self.props)}>{children_html}</div>" 