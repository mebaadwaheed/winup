from .flex import Flex
from ..component import Component
from typing import Dict, Any, Optional, List

class Column(Flex):
    """A layout component that arranges its children in a vertical column."""

    def __init__(self, children: Optional[List[Component]] = None, props: Optional[Dict[str, Any]] = None, **kwargs):
        all_props = (props or {}) | kwargs
        
        # Force the flex direction to be 'column'
        all_props['direction'] = 'column'
        
        super().__init__(children=children, props=all_props) 