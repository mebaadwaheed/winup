from ..component import Component
from ..utils import props_to_html
from typing import Dict, Any, Optional

class Image(Component):
    """An image component that renders an <img> tag."""

    def __init__(self, src: str = "", alt: str = "", props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        all_props['src'] = src
        all_props['alt'] = alt

        super().__init__(props=all_props)

    def render(self) -> str:
        """Renders the image as an HTML <img> element."""
        return f"<img{props_to_html(self.props)}>" 