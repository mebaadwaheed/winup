import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from winup import web
except ImportError:
    print("Please install web dependencies first: pip install .[web]")
    sys.exit(1)

# --- 1. Page Components ---
@web.component
def HomePage():
    return web.ui.Label("Welcome to the Home Page!", style={'font-size': '1.5rem'})

@web.component
def AboutPage():
    return web.ui.Label("This is the About Page.", style={'font-size': '1.5rem'})

@web.component
def SettingsPage():
    return web.ui.Column(children=[
        web.ui.Label("Settings", style={'font-size': '1.5rem'}),
        web.ui.CheckBox(props={'id': 'check1'}),
        web.ui.Label("Enable dark mode")
    ])

# --- 2. App Shell Component ---
# This component provides the main layout and contains the RouterView
@web.component
def AppShell():
    return web.ui.Column(gap="1rem", children=[
        # Navigation bar
        web.ui.Row(
            gap="1.5rem",
            style={
                'padding': '1rem 2rem',
                'background_color': '#2c3e50',
                'color': 'white'
            },
            children=[
                web.RouterLink(to="/", text="Home", style={'color': 'white'}),
                web.RouterLink(to="/about", text="About", style={'color': 'white'}),
                web.RouterLink(to="/settings", text="Settings", style={'color': 'white'}),
            ]
        ),
        # Main content area
        web.ui.Column(
            style={'padding': '2rem'},
            children=[
                # The RouterView is where the page components will be injected
                web.RouterView()
            ]
        )
    ])

# --- 3. Router Definition ---
app_router = web.Router(
    routes={
        '/': HomePage,
        '/about': AboutPage,
        '/settings': SettingsPage,
    }
)

# --- 4. Run the App ---
if __name__ == "__main__":
    web.web_run(
        router_path="web_routing_test:app_router",
        app_shell_path="web_routing_test:AppShell",
        title="Web Routing Test",
        reload=True
    )