from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional, List, Tuple

class Grid(Component):
    """
    A layout component that arranges children in a grid.
    Children should be provided as a list of tuples:
    (component, row, col, row_span, col_span)
    """

    def __init__(self, children: Optional[List[Tuple[Component, int, int, int, int]]] = None, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        
        default_style = {
            'display': 'grid',
            'gap': all_props.pop('gap', '10px'),
            'grid-template-columns': all_props.pop('grid_template_columns', 'repeat(12, 1fr)'),
        }

        user_style = all_props.get('style', {})
        all_props['style'] = default_style | user_style

        # Pass an empty list to the parent, as we handle children specially
        super().__init__(children=[], props=all_props)
        
        # Store the grid children separately
        self.grid_children = children or []

    def render(self) -> str:
        """Renders the grid container and places its children."""
        children_html = []
        for child_tuple in self.grid_children:
            try:
                component, r, c, rs, cs = child_tuple
            except ValueError:
                raise ValueError("Grid children must be a tuple of (component, row, col, row_span, col_span)")
            
            # Apply grid positioning to the child's style
            grid_area_style = f"{r + 1} / {c + 1} / span {rs} / span {cs}"
            
            # This is a safe way to modify the child's props before rendering
            if 'style' not in component.props:
                component.props['style'] = {}
            component.props['style']['grid-area'] = grid_area_style
            
            children_html.append(component.render())

        return f"<div{props_to_html(self.props)}>{''.join(children_html)}</div>" 