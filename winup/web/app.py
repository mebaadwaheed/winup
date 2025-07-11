import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, Callable
import os
import logging
import json
from uvicorn.config import LOGGING_CONFIG

from ..core.hot_reload import _import_from_string
from .script_manager import script_manager
from .router import Router
from ..state import state
from .event_manager import event_manager
from . import profiler

class UvicornLogMessageFilter(logging.Filter):
    """A custom log filter to rebrand Uvicorn's startup message."""
    def filter(self, record):
        if record.name.startswith('uvicorn') and isinstance(record.msg, str):
            record.msg = record.msg.replace("Uvicorn", "WinUp")
        return True

app = FastAPI()
_RUN_CONFIG = {} # Global to hold config for non-reload mode

def _configure_app_routes(config: dict):
    """Adds routes to the global 'app' based on the provided config."""
    
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    templates = Jinja2Templates(directory=templates_dir)
    
    title = config.get("title", "My App")
    favicon = config.get("favicon")
    app_shell_path = config.get("app_shell_path")
    mode = config.get("mode", "router") # Default to router for older configs

    main_component_func = None
    router = None
    
    # --- Get the router object or create one ---
    if mode == "router":
        router = _import_from_string(config["path"])
    else: # mode == "main_component"
        main_component_func = _import_from_string(config["path"])
        router = Router({"/": main_component_func})

    @app.get("/{path:path}", response_class=HTMLResponse)
    async def serve_page(request: Request, path: str):
        
        if mode == 'main_component':
            target_component_func = main_component_func
        else: # mode == 'router'
            route_path = f"/{path or ''}"
            if route_path == "/" and not router.routes.get("/"):
                # Handle root path when only / is not defined
                route_path = next(iter(router.routes))
            
            target_component_func = router.routes.get(route_path)

        if not target_component_func:
            return templates.TemplateResponse("404.html", {"request": request, "title": "Not Found", "path": path}, status_code=404)
        
        if isinstance(target_component_func, dict) and 'redirect' in target_component_func:
            return RedirectResponse(url=target_component_func['redirect'])
        
        # --- Ensure the target is a callable component ---
        if not isinstance(target_component_func, Callable):
            return HTMLResponse("Invalid route configuration: target is not callable.", status_code=500)

        script_manager.reset()
        
        # --- Render the content ---
        page_content_html = target_component_func().render()
        
        # --- Handle App Shell with RouterView ---
        if app_shell_path:
            app_shell_component = _import_from_string(app_shell_path)
            shell_html = app_shell_component().render()
            # Inject the page content into the shell
            final_html = shell_html.replace("<winup-router-view></winup-router-view>", page_content_html)
        else:
            final_html = page_content_html
            
        lifecycle_script = script_manager.generate_script()
        return templates.TemplateResponse("index.html", {"request": request, "title": title, "favicon": favicon, "content": final_html, "lifecycle_script": lifecycle_script})

async def startup_event():
    """Configures routes when the app starts, avoiding import cycles."""
    if "WINUP_WEB_CONFIG" in os.environ: # Reload mode
        config = json.loads(os.environ["WINUP_WEB_CONFIG"])
        _configure_app_routes(config)
    elif _RUN_CONFIG: # Normal mode
        _configure_app_routes(_RUN_CONFIG)

app.on_event("startup")(startup_event)

# Add an endpoint to fetch profiler results
@app.get("/_winup/profiler")
async def get_profiler_results():
    """Returns the current profiler statistics as JSON."""
    return profiler.get_profiler().get_results()

# Mount the static directory to serve winup.js
web_dir = os.path.dirname(os.path.abspath(__file__))
static_dir_path = os.path.join(web_dir, 'static')
app.mount("/_winup/static", StaticFiles(directory=static_dir_path), name="static")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """The main WebSocket endpoint for state synchronization."""
    await websocket.accept()
    state.add_web_connection(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            # --- State updates from client (two-way binding) ---
            if data.get("type") == "state_set":
                key, value = data.get("key"), data.get("value")
                if key:
                    await state.set(key, value) # Broadcasts to all clients
            
            # --- Event triggers from client ---
            elif data.get("type") == "trigger_event":
                event_id = data.get("event_id")
                if event_id:
                    # Pass a dummy event object for now for signature compatibility
                    await event_manager.trigger_event(event_id, {})

    except Exception:
        # Client disconnected, no need to log this as an error
        pass
    finally:
        state.remove_web_connection(websocket)

def web_run(
    main_component_path: Optional[str] = None,
    router_path: Optional[str] = None,
    app_shell_path: Optional[str] = None,
    port: int = 8000,
    title: str = "My App",
    favicon: Optional[str] = None,
    reload: bool = False,
):
    if main_component_path and router_path:
        raise ValueError("You cannot provide both 'main_component_path' and 'router_path'.")
    if app_shell_path and not router_path:
        raise ValueError("'app_shell_path' can only be used with 'router_path'.")
    if not main_component_path and not router_path:
        raise ValueError("You must provide either 'main_component_path' or 'router_path'.")

    # --- Create config dict ---
    run_config = {"title": title, "favicon": favicon, "app_shell_path": app_shell_path}
    if router_path:
        run_config["mode"] = "router"
        run_config["path"] = router_path
    else:
        run_config["mode"] = "main_component"
        run_config["path"] = main_component_path

    # --- Set web context for state manager ---
    state.set_web_context(True)

    # --- Run Server ---
    log_config = LOGGING_CONFIG.copy() # Configure logging for branding
    log_config["filters"] = {"winup_filter": {"()": "winup.web.app.UvicornLogMessageFilter"}}
    if 'filters' not in log_config['handlers']['default']: log_config['handlers']['default']['filters'] = []
    log_config['handlers']['default']['filters'].append('winup_filter')

    if reload:
        # In reload mode, pass config via environment variables
        os.environ["WINUP_WEB_CONFIG"] = json.dumps(run_config)
        uvicorn.run("winup.web.app:app", host="127.0.0.1", port=port, log_config=log_config, reload=True)
    else:
        # In normal mode, configure the app directly
        event_manager.clear()
        global _RUN_CONFIG
        _RUN_CONFIG = run_config
        uvicorn.run(app, host="127.0.0.1", port=port, log_config=log_config) 