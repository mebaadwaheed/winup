# winup/router/router.py
from typing import Dict, Callable, Optional
import winup
from winup import ui
from winup.core.component import Component
from winup.ui import clear_layout
from winup.core.memoize import clear_memo_cache
import re
import inspect

class Router:
    """Manages navigation and application state for different UI views."""
    def __init__(self, routes: Dict[str, any]):
        if not routes:
            raise ValueError("Router must be initialized with at least one route.")
        
        self.routes = self._compile_routes(routes)
        # Find the first path that doesn't have a redirect.
        initial_path = next((original_path for _, _, _, original_path, redirect in self.routes if not redirect), list(routes.keys())[0])

        self.state = winup.state.create("router_current_path", initial_path)

    def _compile_routes(self, routes: Dict, base_path: str = ""):
        """
        Recursively compiles route strings into regex, handling nested routes.
        Each route can be a component or a dict with 'component' and 'children'.
        It can also contain a 'redirect' key.
        """
        compiled = []
        for path, value in routes.items():
            current_path = f"{base_path}{path}".replace("//", "/")
            
            component_factory = None
            children = {}
            redirect = None

            if isinstance(value, dict):
                component_factory = value.get("component")
                children = value.get("children", {})
                redirect = value.get("redirect")
            else:
                component_factory = value
            
            if component_factory or redirect:
                param_keys = re.findall(r":(\w+)", current_path)
                regex_path = re.sub(r":\w+", r"([^/]+)", current_path) + "$"
                compiled.append((re.compile(regex_path), param_keys, component_factory, current_path, redirect))

            if children:
                compiled.extend(self._compile_routes(children, base_path=current_path))
        
        return compiled

    def navigate(self, path: str):
        """Navigates to the given path, handling redirects and matching against registered routes."""
        component, params, redirect = self._get_route_info_for_path(path)
        
        if redirect:
            self.navigate(redirect) # Recursive call for the new path
            return

        if component:
            self.state.set(path)
        else:
            print(f"Error: Route for '{path}' not found.")

    def _get_route_info_for_path(self, path: str) -> tuple[Optional[Callable], Optional[dict], Optional[str]]:
        """Finds route info for a given path: (component, params, redirect)."""
        for regex, param_keys, component_factory, original_path, redirect in self.routes:
            match = regex.match(path)
            if match:
                param_values = match.groups()
                params = dict(zip(param_keys, param_values))
                # Check for a redirect first
                if redirect:
                    # Perform parameter substitution in the redirect path
                    for key, val in params.items():
                        redirect = redirect.replace(f":{key}", val)
                    return None, None, redirect
                return component_factory, params, None
        return None, None, None

    def get_component_for_path(self, path: str) -> Optional[tuple[Callable[..., Component], dict]]:
        """
        Finds the component factory for a given path and extracts route parameters.
        This is used by RouterView. It ignores redirects as navigation is already complete.
        """
        for regex, param_keys, component_factory, _, _ in self.routes:
            match = regex.match(path)
            if match:
                param_values = match.groups()
                params = dict(zip(param_keys, param_values))
                return component_factory, params
        return None

@winup.component
def RouterView(router: Router) -> Component:
    """
    A component that displays the view for the current route.
    It listens to route changes and updates its content automatically.
    """
    # Create a container that will hold the routed components.
    view_container = ui.Frame()
    view_container.set_layout("vertical")

    def _update_view(path: str):
        """Clears the container and renders the new component with route params."""
        result = router.get_component_for_path(path)
        if result:
            component_factory, params = result
            # Clear previous component from the container
            if view_container.layout() is not None:
                ui.clear_layout(view_container.layout())
            
            # Check if the component needs the router instance passed to it
            # Use the pre-computed __signature__ to avoid recursion with inspect.
            if hasattr(component_factory, '__signature__'):
                sig = component_factory.__signature__
                if 'router' in sig.parameters:
                    params['router'] = router

            # Instantiate and add the new component, passing params to it
            new_component = component_factory(**params)
            view_container.layout().addWidget(new_component)

    # Subscribe to changes in the router's state.
    router.state.subscribe(_update_view)
    
    # Perform the initial render for the starting route.
    _update_view(router.state.get())

    return view_container

@winup.component
def RouterLink(router: Router, to: str, text: str, props: Dict = None) -> Component:
    """
    A navigational component that looks like a hyperlink and triggers a route change on click.
    """
    def handle_click():
        router.navigate(to)

    # Use a Button styled as a link for better control and consistency.
    link_props = {
        "font-family": "Segoe UI",
        "text-decoration": "none",
        "color": "#0078D4",
        "border": "none",
        "background-color": "transparent",
        "cursor": "PointingHandCursor",
        "text-align": "left",
        "padding": "0"
    }
    
    # Merge user-defined props
    if props:
        link_props.update(props)

    return ui.Button(text, on_click=handle_click, props=link_props) 