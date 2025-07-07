from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional
from typing import List as ListType

class BulletedList(Component):
    """A list component that renders children as <li> items."""

    def __init__(self, children: Optional[ListType[Component]] = None, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        
        # Default to a <ul> but allow <ol> via props
        self.tag = all_props.pop('tag', 'ul')
        if self.tag not in ['ul', 'ol']:
            self.tag = 'ul'

        super().__init__(children=children, props=all_props)

    def render(self) -> str:
        """Renders the list and its children wrapped in <li>."""
        children_html = "".join(f"<li>{child.render()}</li>" for child in self.children)
        return f"<{self.tag}{props_to_html(self.props)}>{children_html}</{self.tag}>" 