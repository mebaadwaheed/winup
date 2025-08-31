"""
Unified routing test using the enhanced @component decorator with platform parameters.
This test demonstrates routing that works on both desktop and web platforms.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, component
from winup.core.platform import get_current_platform

# Import web components for routing
try:
    from winup import web
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

# --- 1. Cross-Platform Page Components ---

@component(web=True, desktop=True)
def HomePage():
    """Home page component that works on both platforms."""
    platform = get_current_platform()
    
    if platform == 'web':
        return web.ui.Column(children=[
            web.ui.Label("🏠 Welcome to the Home Page!", style={'font-size': '1.5rem', 'color': '#2c3e50'}),
            web.ui.Label(f"Running on: {platform}", style={'font-size': '1rem', 'color': '#7f8c8d'}),
            web.ui.Button("Home Action", style={'margin-top': '1rem'})
        ])
    else:
        return ui.Column(
            children=[
                ui.Label("🏠 Welcome to the Home Page!", props={"font-size": "18px", "font-weight": "bold"}),
                ui.Label(f"Running on: {platform}", props={"margin-top": "10px"}),
                ui.Button("Home Action", props={"margin-top": "15px"})
            ],
            props={"padding": "20px", "spacing": 15}
        )

@component(web=True, desktop=True)
def AboutPage():
    """About page component that works on both platforms."""
    platform = get_current_platform()
    
    if platform == 'web':
        return web.ui.Column(children=[
            web.ui.Label("ℹ️ About This App", style={'font-size': '1.5rem', 'color': '#2c3e50'}),
            web.ui.Label("This is a unified routing demo showing cross-platform components.", 
                        style={'font-size': '1rem', 'margin-top': '1rem'}),
            web.ui.Label(f"Current platform: {platform}", style={'color': '#7f8c8d'})
        ])
    else:
        return ui.Column(
            children=[
                ui.Label("ℹ️ About This App", props={"font-size": "18px", "font-weight": "bold"}),
                ui.Label("This is a unified routing demo showing cross-platform components.", 
                        props={"margin-top": "10px"}),
                ui.Label(f"Current platform: {platform}", props={"margin-top": "10px", "color": "gray"})
            ],
            props={"padding": "20px", "spacing": 15}
        )

@component(web=True, desktop=True)
def SettingsPage():
    """Settings page component that works on both platforms."""
    platform = get_current_platform()
    
    if platform == 'web':
        return web.ui.Column(children=[
            web.ui.Label("⚙️ Settings", style={'font-size': '1.5rem', 'color': '#2c3e50'}),
            web.ui.CheckBox(props={'id': 'darkmode'}),
            web.ui.Label("Enable dark mode", style={'margin-left': '0.5rem'}),
            web.ui.Button("Save Settings", style={'margin-top': '1rem', 'background-color': '#27ae60', 'color': 'white'})
        ])
    else:
        return ui.Column(
            children=[
                ui.Label("⚙️ Settings", props={"font-size": "18px", "font-weight": "bold"}),
                ui.Checkbox("Enable dark mode", props={"margin-top": "15px"}),
                ui.Button("Save Settings", props={"margin-top": "15px", "background-color": "#27ae60"})
            ],
            props={"padding": "20px", "spacing": 15}
        )

# --- 2. App Shell Component (Web Only) ---

@component(web=True, desktop=False)
def AppShell():
    """App shell with navigation - web only."""
    if not WEB_AVAILABLE:
        return "<div>Web dependencies not available</div>"
        
    return web.ui.Column(gap="1rem", children=[
        # Navigation bar
        web.ui.Row(
            gap="1.5rem",
            style={
                'padding': '1rem 2rem',
                'background-color': '#2c3e50',
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

# --- 3. Desktop Navigation Component ---

@component(web=False, desktop=True)
def DesktopApp():
    """Desktop app with tab-based navigation."""
    return ui.TabView(
        tabs=[
            {"title": "Home", "content": HomePage()},
            {"title": "About", "content": AboutPage()},
            {"title": "Settings", "content": SettingsPage()}
        ],
        props={"padding": "10px"}
    )

# --- 4. Router Definition (Web Only) ---

if WEB_AVAILABLE:
    app_router = web.Router(
        routes={
            '/': HomePage,
            '/about': AboutPage,
            '/settings': SettingsPage,
        }
    )

# --- 5. Platform-Specific Entry Points ---

def run_desktop():
    """Run in desktop mode with tab navigation."""
    winup.run("tests.unified_routing_test:DesktopApp", 
             title="Unified Routing Test - Desktop", 
             width=700, height=500)

def run_web():
    """Run in web mode with router navigation."""
    if not WEB_AVAILABLE:
        print("Web dependencies not installed. Install with 'pip install winup[web]'")
        return
        
    web.web_run(
        router_path="tests.unified_routing_test:app_router",
        app_shell_path="tests.unified_routing_test:AppShell",
        title="Unified Routing Test - Web",
        port=8003,
        reload=True
    )

if __name__ == "__main__":
    platform = get_current_platform()
    print(f"Running unified routing test on {platform} platform...")
    
    if platform == 'web':
        run_web()
    else:
        run_desktop()
