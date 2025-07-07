from .flex import Flex
from ..component import Component
from typing import Dict, Any, Optional, List

class Row(Flex):
    """A layout component that arranges its children in a horizontal row."""

    def __init__(self, children: Optional[List[Component]] = None, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        
        # Force the flex direction to be 'row'
        all_props['direction'] = 'row'
        
        super().__init__(children=children, props=all_props) 