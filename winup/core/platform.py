"""
Platform detection and utilities for WinUp components.
"""
import os
from typing import Set, Optional

# Global platform context - can be set by the application
_current_platform: Optional[str] = None

def set_platform(platform: str):
    """Set the current platform context."""
    global _current_platform
    if platform not in {'web', 'desktop'}:
        raise ValueError(f"Invalid platform '{platform}'. Must be 'web' or 'desktop'.")
    _current_platform = platform

def get_current_platform() -> str:
    """Get the current platform context."""
    global _current_platform
    
    if _current_platform:
        return _current_platform
    
    # Auto-detect platform based on environment
    # This is a simple heuristic - can be enhanced
    try:
        # If we can import PySide6, assume desktop
        import PySide6
        return 'desktop'
    except ImportError:
        # If PySide6 not available, assume web
        return 'web'

def is_platform_supported(component_func, platform: str = None) -> bool:
    """Check if a component supports the given platform."""
    if platform is None:
        platform = get_current_platform()
    
    if hasattr(component_func, '_winup_platforms'):
        return platform in component_func._winup_platforms
    
    # If no platform info, assume it supports the current platform
    return True

def get_supported_platforms(component_func) -> Set[str]:
    """Get the set of platforms supported by a component."""
    if hasattr(component_func, '_winup_platforms'):
        return component_func._winup_platforms.copy()
    
    # If no platform info, assume desktop (legacy behavior)
    return {'desktop'}

def validate_platform_compatibility(component_func, platform: str = None):
    """Validate that a component is compatible with the current platform."""
    if platform is None:
        platform = get_current_platform()
    
    if not is_platform_supported(component_func, platform):
        supported = get_supported_platforms(component_func)
        raise RuntimeError(
            f"Component '{component_func.__name__}' does not support platform '{platform}'. "
            f"Supported platforms: {', '.join(sorted(supported))}"
        )
