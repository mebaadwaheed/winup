"""
Test the unified @component decorator with platform parameters.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui, component
from winup.core.platform import set_platform, get_current_platform

# Test different platform configurations

@component
def DesktopOnlyComponent():
    """Default component - desktop only"""
    return ui.Label("Desktop Only Component")

@component(web=True, desktop=False)
def WebOnlyComponent():
    """Web-only component"""
    return ui.Label("Web Only Component")

@component(web=True, desktop=True)
def CrossPlatformComponent():
    """Component that works on both platforms"""
    current = get_current_platform()
    return ui.Label(f"Cross-platform Component (running on {current})")

@component(platforms=['web', 'desktop'])
def UniversalComponent():
    """Another way to specify cross-platform support"""
    return ui.Label("Universal Component")

@component
def App():
    """Main test application"""
    current_platform = get_current_platform()
    
    return ui.Column(
        children=[
            ui.Label(f"Current Platform: {current_platform}", 
                    props={"font-weight": "bold", "font-size": "16px"}),
            ui.Label("Testing Platform-Aware Components:", 
                    props={"margin-top": "20px", "font-weight": "bold"}),
            
            # This should always work (desktop default)
            DesktopOnlyComponent(),
            
            # This should work on both platforms
            CrossPlatformComponent(),
            UniversalComponent(),
            
            # Test platform info display
            ui.Label(f"DesktopOnlyComponent platforms: {getattr(DesktopOnlyComponent, '_winup_platforms', 'None')}"),
            ui.Label(f"WebOnlyComponent platforms: {getattr(WebOnlyComponent, '_winup_platforms', 'None')}"),
            ui.Label(f"CrossPlatformComponent platforms: {getattr(CrossPlatformComponent, '_winup_platforms', 'None')}"),
        ],
        props={"padding": "20px", "spacing": 10}
    )

if __name__ == "__main__":
    # Test desktop mode - no need to call set_platform manually anymore
    print("Testing desktop platform...")
    winup.run("tests.platform_component_test:App", title="Platform Component Test", width=600, height=400)
