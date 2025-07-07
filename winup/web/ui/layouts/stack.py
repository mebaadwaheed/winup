from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional, List

class Stack(Component):
    """
    A layout component that stacks children on top of each other,
    showing only one at a time.
    """

    def __init__(self, children: Optional[List[Component]] = None, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        
        default_style = {
            'display': 'grid',
            'grid-template-areas': '"stack-area"',
        }
        
        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style
        
        super().__init__(children=children, props=all_props)
        self.active_child_index = all_props.pop('active_child_index', 0)

    def render(self) -> str:
        """Renders the stack container and its children."""
        children_html = []
        for i, child in enumerate(self.children):
            # All children are placed in the same grid area
            if 'style' not in child.props:
                child.props['style'] = {}
            child.props['style']['grid-area'] = 'stack-area'
            
            # Hide children that are not the active one
            if i != self.active_child_index:
                child.props['style']['display'] = 'none'
            else:
                child.props['style'].pop('display', None)

            children_html.append(child.render())

        return f"<div{props_to_html(self.props)}>{''.join(children_html)}</div>" 