# winup/web/router.py
from .ui.component import Component
from .ui.utils import props_to_html
from .ui.widgets.link import Link
from typing import Dict, Any, Optional, Callable

class Router:
    """Holds the routing configuration for the application."""
    def __init__(self, routes: Dict[str, Callable]):
        self.routes = routes

class RouterLink(Link):
    """A styled link for navigating between router paths within an app shell."""
    def __init__(self, to: str, text: str, **kwargs):
        super().__init__(text=text, href=to, **kwargs)
        
        default_style = {
            'color': '#007bff',
            'text_decoration': 'none',
            'padding': '0.5rem 1rem',
            'border_radius': '5px',
            'transition': 'background-color 0.2s',
        }
        user_style = self.props.get('style', {})
        self.props['style'] = default_style | user_style

class RouterView(Component):
    """A placeholder component that the server will replace with the correct page."""
    def render(self) -> str:
        # This special tag will be found and replaced by the server.
        return "<winup-router-view></winup-router-view>"

# We don't need a RouterView component for the web, as FastAPI's routing
# mechanism combined with web_run will serve this purpose. 