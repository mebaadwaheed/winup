from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional

class Label(Component):
    def __init__(self, text: str = "", props: Optional[Dict[str, Any]] = None, **kwargs):
        # Merge kwargs into props for a more convenient API
        all_props = (props or {}) | kwargs
        super().__init__(props=all_props)
        self.text = text

    def render(self) -> str:
        # Get props from the instance, but allow overriding from the text property
        all_props = self.props.copy()
        text = self.text
        if 'text' in all_props:
            text = all_props.pop('text')
            
        return f"<p{props_to_html(all_props)}>{text}</p>" 