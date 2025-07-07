from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional

class CheckBox(Component):
    """A checkbox input component that supports two-way state binding."""

    def __init__(self, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        all_props['type'] = 'checkbox'
        
        super().__init__(props=all_props)

    def render(self) -> str:
        """Renders the checkbox as an HTML <input> element."""
        return f"<input{props_to_html(self.props)}>" 