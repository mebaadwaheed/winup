# WinUp Component Decorator Documentation

## Overview

The `@component` decorator is the unified way to create cross-platform components in WinUp that work seamlessly across desktop (Qt) and web (HTML) platforms.

## Basic Syntax

```python
from winup import component

@component
def MyComponent():
    """Default desktop-only component"""
    return ui.Label("Hello Desktop!")

@component(web=True, desktop=False)
def WebOnlyComponent():
    """Web-only component"""
    return ui.Label("Hello Web!")

@component(web=True, desktop=True)
def CrossPlatformComponent():
    """Works on both platforms"""
    return ui.Label("Hello Cross-Platform!")

@component(platforms=['web', 'desktop'])
def AlternativeCrossPlatform():
    """Alternative syntax for cross-platform"""
    return ui.Label("Hello Alternative!")
```

## Platform Parameters

### `web` (bool, default: False)
- **True**: Component can run on web platform
- **False**: Component cannot run on web platform
- When `web=True` and current platform is 'web', components return function results directly for HTML rendering

### `desktop` (bool, default: True)
- **True**: Component can run on desktop platform  
- **False**: Component cannot run on desktop platform
- When `desktop=True` and current platform is 'desktop', components use Qt widget wrapper behavior

### `platforms` (list, optional)
- Alternative syntax: `platforms=['web', 'desktop']`
- Equivalent to `web=True, desktop=True`
- Accepts list of platform strings

## Platform Detection

Components automatically detect the current platform using `get_current_platform()`:

```python
from winup.core.platform import get_current_platform

@component(web=True, desktop=True)
def AdaptiveComponent():
    platform = get_current_platform()
    if platform == 'web':
        return ui.Label("Running on Web", props={"color": "blue"})
    else:
        return ui.Label("Running on Desktop", props={"color": "green"})
```

## Platform Validation

Components validate platform compatibility at runtime:

```python
@component(web=False, desktop=True)  # Desktop only
def DesktopOnlyComponent():
    return ui.Label("Desktop Only")

# This will throw an error if run on web platform:
# PlatformError: Component 'DesktopOnlyComponent' is not supported on platform 'web'
```

## Cross-Platform Best Practices

### 1. Use Platform-Agnostic Props
```python
@component(web=True, desktop=True)
def StyledComponent():
    return ui.Button(
        "Click Me",
        props={
            "background-color": "#007bff",  # Works on both platforms
            "color": "white",
            "padding": "10px 20px",
            "border-radius": "5px"
        }
    )
```

### 2. Platform-Specific Styling
```python
@component(web=True, desktop=True)
def PlatformSpecificComponent():
    platform = get_current_platform()
    
    if platform == 'web':
        props = {"box-shadow": "0 2px 4px rgba(0,0,0,0.1)"}
    else:
        props = {"border": "1px solid #ccc"}
    
    return ui.Frame(
        children=[ui.Label("Adaptive Styling")],
        props=props
    )
```

### 3. Responsive Layouts
```python
@component(web=True, desktop=True)
def ResponsiveLayout():
    return ui.Row(
        children=[
            ui.Column(
                children=[ui.Label("Left")],
                props={"flex": "1", "padding": "10px"}
            ),
            ui.Column(
                children=[ui.Label("Right")],
                props={"flex": "2", "padding": "10px"}
            )
        ],
        props={"spacing": 10}
    )
```

## Component Registration

The decorator automatically registers components with the appropriate platform handlers:

- **Desktop**: Components are wrapped in Qt Component class
- **Web**: Components return HTML elements directly
- **Cross-platform**: Behavior adapts based on current platform

## Error Handling

### Platform Compatibility Errors
```python
# Will raise PlatformError if used on unsupported platform
@component(web=False, desktop=True)
def DesktopOnly():
    return ui.Label("Desktop Only")
```

### Invalid Platform Parameters
```python
# Will raise ValueError during decorator application
@component(platforms=['invalid_platform'])
def InvalidComponent():
    return ui.Label("Invalid")
```

## Migration from Separate Decorators

### Before (Deprecated)
```python
from winup.web import web_component

@web_component
def OldWebComponent():
    return ui.Label("Web Only")
```

### After (Unified)
```python
from winup import component

@component(web=True, desktop=False)
def NewWebComponent():
    return ui.Label("Web Only")
```

## Advanced Usage

### Dynamic Platform Selection
```python
@component(web=True, desktop=True)
def DynamicComponent():
    platform = get_current_platform()
    
    # Platform-specific logic
    if platform == 'web':
        return ui.Column(
            children=[
                ui.Label("Web Interface"),
                ui.Button("Web Button", props={"onclick": "alert('Web!')"})
            ]
        )
    else:
        return ui.Column(
            children=[
                ui.Label("Desktop Interface"),
                ui.Button("Desktop Button", on_click=lambda: print("Desktop!"))
            ]
        )
```

### Component Composition
```python
@component(web=True, desktop=True)
def Header():
    return ui.Label("Header", props={"font-size": "24px", "font-weight": "bold"})

@component(web=True, desktop=True)
def Footer():
    return ui.Label("Footer", props={"font-size": "12px", "color": "#666"})

@component(web=True, desktop=True)
def App():
    return ui.Column(
        children=[
            Header(),
            ui.Label("Content"),
            Footer()
        ],
        props={"spacing": 20}
    )
```

## Platform-Specific Features

### Desktop-Only Features
- Qt-specific properties (objectName, cursor shapes)
- Native Qt layouts and sizing policies
- Desktop window management

### Web-Only Features  
- HTML attributes (onclick, onchange, etc.)
- CSS flexbox and grid properties
- DOM manipulation capabilities

### Shared Features
- Basic styling (colors, fonts, spacing)
- Layout components (Row, Column, Grid)
- Event handling (adapted per platform)
- State management and binding
