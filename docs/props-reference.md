# WinUp Props Reference Guide

## Overview

This comprehensive guide covers all available props in WinUp, their behavior on desktop vs web platforms, accepted values, and usage examples.

## Special Properties

### Platform Control
| Prop | Desktop | Web | Values | Description |
|------|---------|-----|--------|-------------|
| `class` | QSS class selector | CSS class | string | Applies CSS/QSS class for styling |
| `id` | QSS ID selector | HTML ID | string | Unique identifier for targeting |
| `objectName` | QSS ID selector | HTML ID | string | Alias for `id` |

### Text Properties
| Prop | Desktop | Web | Values | Description |
|------|---------|-----|--------|-------------|
| `font-size` | QFont.setPointSize() | CSS font-size | "12px", "16px", integer | Text size |
| `font-weight` | QFont.setWeight() | CSS font-weight | "thin", "light", "normal", "medium", "bold", "extrabold", "black" | Text weight |
| `color` | QSS color | CSS color | "#ff0000", "red", "rgb(255,0,0)" | Text color |
| `placeholder-text` | setPlaceholderText() | HTML placeholder | string | Input placeholder text |
| `text-align` | QSS text-align | CSS text-align | "left", "center", "right", "justify" | Text alignment |

### Layout Properties
| Prop | Desktop | Web | Values | Description |
|------|---------|-----|--------|-------------|
| `flex` | Layout stretch factor | CSS flex | "1", "2", integer | Flex grow factor |
| `alignment` | Qt.AlignmentFlag | CSS align-items | "AlignLeft", "AlignCenter", "AlignRight", "AlignTop", "AlignBottom" | Widget alignment |
| `spacing` | Layout spacing | CSS gap | integer (pixels) | Space between children |
| `padding` | QSS padding | CSS padding | "10px", "10px 20px", "5px 10px 15px 20px" | Inner spacing |
| `margin` | QSS margin | CSS margin | "10px", "10px 20px", "5px 10px 15px 20px" | Outer spacing |

### Visual Properties
| Prop | Desktop | Web | Values | Description |
|------|---------|-----|--------|-------------|
| `background-color` | QSS background-color | CSS background-color | "#ffffff", "white", "rgb(255,255,255)" | Background color |
| `border` | QSS border | CSS border | "1px solid #ccc", "2px dashed red" | Border styling |
| `border-radius` | QSS border-radius | CSS border-radius | "5px", "10px 5px", "50%" | Rounded corners |
| `width` | setFixedWidth() | CSS width | "100px", "50%", "auto" | Widget width |
| `height` | setFixedHeight() | CSS height | "100px", "50%", "auto" | Widget height |
| `opacity` | QSS opacity | CSS opacity | 0.0 to 1.0 | Transparency level |

### Interaction Properties
| Prop | Desktop | Web | Values | Description |
|------|---------|-----|--------|-------------|
| `cursor` | setCursor() | CSS cursor | "ArrowCursor", "PointingHandCursor", "WaitCursor" | Mouse cursor style |
| `read-only` | setReadOnly() | HTML readonly | true, false | Input read-only state |
| `disabled` | setDisabled() | HTML disabled | true, false | Widget disabled state |

### Web-Specific Properties
| Prop | Desktop | Web | Values | Description |
|------|---------|-----|--------|-------------|
| `onclick` | ❌ Ignored | JavaScript event | "alert('clicked')" | Click event handler |
| `onchange` | ❌ Ignored | JavaScript event | "handleChange()" | Change event handler |
| `onsubmit` | ❌ Ignored | JavaScript event | "submitForm()" | Form submit handler |
| `type` | ❌ Ignored | HTML input type | "text", "password", "email", "number" | Input field type |
| `href` | ❌ Ignored | HTML href | "https://example.com" | Link destination |
| `target` | ❌ Ignored | HTML target | "_blank", "_self" | Link target |

### Desktop-Specific Properties
| Prop | Desktop | Web | Values | Description |
|------|---------|-----|--------|-------------|
| `tabs` | Tab count for links | ❌ Ignored | integer | Number of tabs to open |

## Cursor Types (Desktop)

| Value | Description |
|-------|-------------|
| `ArrowCursor` | Standard arrow cursor |
| `UpArrowCursor` | Upward pointing arrow |
| `CrossCursor` | Cross/plus cursor |
| `WaitCursor` | Hourglass/wait cursor |
| `IBeamCursor` | Text selection cursor |
| `SizeVerCursor` | Vertical resize cursor |
| `SizeHorCursor` | Horizontal resize cursor |
| `SizeBDiagCursor` | Diagonal resize cursor (\\) |
| `SizeFDiagCursor` | Diagonal resize cursor (/) |
| `SizeAllCursor` | Move/resize all directions |
| `BlankCursor` | Invisible cursor |
| `SplitVCursor` | Vertical split cursor |
| `SplitHCursor` | Horizontal split cursor |
| `PointingHandCursor` | Hand pointer cursor |
| `ForbiddenCursor` | Not allowed cursor |
| `WhatsThisCursor` | Help cursor |
| `BusyCursor` | Busy cursor |
| `OpenHandCursor` | Open hand cursor |
| `ClosedHandCursor` | Closed hand cursor |

## Font Weights

| Value | Desktop (QFont.Weight) | Web (CSS) |
|-------|----------------------|-----------|
| `thin` | Thin | 100 |
| `extralight` | ExtraLight | 200 |
| `light` | Light | 300 |
| `normal` | Normal | 400 |
| `medium` | Medium | 500 |
| `demibold` | DemiBold | 600 |
| `bold` | Bold | 700 |
| `extrabold` | ExtraBold | 800 |
| `black` | Black | 900 |

## Alignment Values

| Value | Desktop (Qt.AlignmentFlag) | Web (CSS) |
|-------|---------------------------|-----------|
| `AlignLeft` | AlignLeft | flex-start |
| `AlignRight` | AlignRight | flex-end |
| `AlignCenter` | AlignCenter | center |
| `AlignTop` | AlignTop | flex-start |
| `AlignBottom` | AlignBottom | flex-end |
| `AlignVCenter` | AlignVCenter | center |

## Color Formats

Both platforms support multiple color formats:

| Format | Example | Description |
|--------|---------|-------------|
| Hex | `#ff0000`, `#f00` | Hexadecimal color codes |
| RGB | `rgb(255, 0, 0)` | RGB function notation |
| RGBA | `rgba(255, 0, 0, 0.5)` | RGB with alpha channel |
| Named | `red`, `blue`, `green` | CSS color names |
| HSL | `hsl(0, 100%, 50%)` | Hue, saturation, lightness |

## Size Units

| Unit | Desktop | Web | Example | Description |
|------|---------|-----|---------|-------------|
| `px` | Pixels | Pixels | "16px" | Absolute pixels |
| `%` | ❌ Limited | Percentage | "50%" | Relative to parent |
| `em` | ❌ No | Relative to font | "1.5em" | Font-relative sizing |
| `rem` | ❌ No | Relative to root | "2rem" | Root font-relative |
| Integer | Pixels | Pixels | 16 | Numeric pixels |

## Tailwind CSS Support

WinUp supports Tailwind CSS classes via the `tailwind` prop:

```python
ui.Button(
    "Styled Button",
    props={
        "tailwind": "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    }
)
```

## Theme Variables

Props support theme variable substitution:

```python
ui.Label(
    "Themed Text",
    props={
        "color": "{{primary-color}}",
        "background-color": "{{background-color}}"
    }
)
```

## Platform-Specific Examples

### Cross-Platform Styling
```python
@component(web=True, desktop=True)
def StyledComponent():
    return ui.Button(
        "Universal Button",
        props={
            "background-color": "#007bff",  # Works on both
            "color": "white",               # Works on both
            "padding": "10px 20px",         # Works on both
            "border-radius": "5px",         # Works on both
            "font-weight": "bold"           # Works on both
        }
    )
```

### Desktop-Specific Features
```python
@component(desktop=True)
def DesktopComponent():
    return ui.Button(
        "Desktop Button",
        props={
            "cursor": "PointingHandCursor",  # Desktop only
            "objectName": "main-button"      # Desktop only
        }
    )
```

### Web-Specific Features
```python
@component(web=True)
def WebComponent():
    return ui.Button(
        "Web Button",
        props={
            "onclick": "alert('Clicked!')",  # Web only
            "type": "submit",                # Web only
            "class": "btn btn-primary"       # Web CSS classes
        }
    )
```

## Layout-Specific Props

### Row/Column Layouts
```python
ui.Row(
    children=[...],
    props={
        "spacing": 10,           # Gap between children
        "alignment": "AlignCenter", # Child alignment
        "padding": "20px",       # Inner spacing
        "background-color": "#f5f5f5"
    }
)
```

### Grid Layouts
```python
ui.Grid(
    children=[
        (ui.Button("1"), 0, 0, 1, 1),  # (widget, row, col, rowspan, colspan)
        (ui.Button("2"), 0, 1, 1, 1),
    ],
    props={
        "padding": "20px",
        "background-color": "#ffffff"
    }
)
```

### Flex Layouts
```python
ui.Column(
    children=[
        ui.Label("Header"),
        ui.Frame(
            children=[ui.Label("Content")],
            props={"flex": "1"}  # Takes remaining space
        ),
        ui.Label("Footer")
    ]
)
```

## Widget-Specific Props

### Input Widgets
```python
ui.Input(
    props={
        "placeholder-text": "Enter text...",
        "font-size": "16px",
        "padding": "8px 12px",
        "border": "1px solid #ddd",
        "border-radius": "4px",
        "read-only": False
    }
)
```

### Button Widgets
```python
ui.Button(
    "Click Me",
    props={
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "padding": "12px 24px",
        "border-radius": "6px",
        "cursor": "PointingHandCursor",
        "font-weight": "bold"
    }
)
```

### Image Widgets
```python
ui.Image(
    src="path/to/image.png",
    props={
        "width": "200px",
        "height": "150px",
        "border-radius": "8px",
        "border": "2px solid #ddd"
    }
)
```

## Responsive Design

### Flexible Sizing
```python
ui.Row(
    children=[
        ui.Column(props={"flex": "1"}),  # 1/3 width
        ui.Column(props={"flex": "2"}),  # 2/3 width
    ]
)
```

### Conditional Styling
```python
from winup.core.platform import get_current_platform

@component(web=True, desktop=True)
def ResponsiveComponent():
    platform = get_current_platform()
    
    base_props = {
        "padding": "20px",
        "background-color": "#f8f9fa"
    }
    
    if platform == 'web':
        base_props.update({
            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "border-radius": "8px"
        })
    else:
        base_props.update({
            "border": "1px solid #dee2e6"
        })
    
    return ui.Frame(
        children=[ui.Label("Responsive Content")],
        props=base_props
    )
```

## Common Patterns

### Card Component
```python
def Card(title, content):
    return ui.Frame(
        children=[
            ui.Label(title, props={"font-weight": "bold", "margin-bottom": "10px"}),
            ui.Label(content)
        ],
        props={
            "padding": "20px",
            "background-color": "white",
            "border-radius": "8px",
            "border": "1px solid #e1e5e9",
            "margin": "10px"
        }
    )
```

### Form Input
```python
def FormInput(label, placeholder):
    return ui.Column(
        children=[
            ui.Label(label, props={"font-weight": "medium", "margin-bottom": "5px"}),
            ui.Input(props={
                "placeholder-text": placeholder,
                "padding": "8px 12px",
                "border": "1px solid #ced4da",
                "border-radius": "4px",
                "font-size": "14px"
            })
        ],
        props={"spacing": 0, "margin-bottom": "15px"}
    )
```

### Button Variants
```python
def PrimaryButton(text):
    return ui.Button(text, props={
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "padding": "10px 20px",
        "border-radius": "5px",
        "font-weight": "medium"
    })

def SecondaryButton(text):
    return ui.Button(text, props={
        "background-color": "transparent",
        "color": "#6c757d",
        "border": "1px solid #6c757d",
        "padding": "10px 20px",
        "border-radius": "5px"
    })
```

## Advanced Styling

### Hover Effects (Web)
```python
ui.Button(
    "Hover Me",
    props={
        "background-color": "#007bff",
        "color": "white",
        "padding": "10px 20px",
        "border-radius": "5px",
        "transition": "background-color 0.3s ease",
        "class": "hover-button"  # Define hover styles in CSS
    }
)
```

### Animation Properties (Web)
```python
ui.Frame(
    children=[...],
    props={
        "transition": "all 0.3s ease",
        "transform": "translateY(0)",
        "opacity": "1"
    }
)
```

### Grid Areas (Web)
```python
ui.Grid(
    children=[
        (ui.Label("Header"), 0, 0, 1, 2),  # Spans 2 columns
        (ui.Label("Sidebar"), 1, 0, 1, 1),
        (ui.Label("Content"), 1, 1, 1, 1),
    ],
    props={
        "display": "grid",
        "grid-template-columns": "200px 1fr",
        "grid-template-rows": "auto 1fr",
        "gap": "10px"
    }
)
```

## Validation and Error Handling

### Invalid Props
```python
# Desktop: Warns about unknown properties
ui.Button("Test", props={"invalid-prop": "value"})
# Warning: Unknown property 'invalid-prop'

# Web: Invalid props are passed through to HTML
ui.Button("Test", props={"data-custom": "value"})  # Valid HTML attribute
```

### Platform Compatibility
```python
# Desktop-only prop on web platform
ui.Input(props={"cursor": "IBeamCursor"})  # Ignored on web

# Web-only prop on desktop platform  
ui.Button("Click", props={"onclick": "alert('hi')"})  # Ignored on desktop
```

## Performance Considerations

### Efficient Styling
```python
# Good: Reuse style objects
button_style = {
    "background-color": "#007bff",
    "color": "white",
    "padding": "10px 20px"
}

ui.Button("Button 1", props=button_style)
ui.Button("Button 2", props=button_style)
```

### Avoid Inline Styles (Web)
```python
# Better: Use CSS classes
ui.Button("Styled", props={"class": "btn-primary"})

# Avoid: Excessive inline styles
ui.Button("Styled", props={
    "background": "linear-gradient(45deg, #ff0000, #00ff00)",
    "box-shadow": "0 4px 8px rgba(0,0,0,0.2)",
    "transform": "rotate(5deg)"
})
```

## Debugging Props

### Enable Prop Warnings
Props that don't apply to the current platform will show warnings in the console:

```
Warning: 'onclick' prop used on a widget that doesn't support it.
Warning: Unknown cursor name 'invalid-cursor'.
Warning: Invalid font-size value 'not-a-number': invalid literal for int()
```

### Inspect Applied Styles
```python
# Desktop: Check Qt stylesheet
widget.styleSheet()

# Web: Check HTML attributes and CSS
# View source in browser developer tools
```

## Migration Guide

### From Platform-Specific to Unified
```python
# Before: Separate implementations
@desktop_component
def DesktopApp():
    return ui.Button("Desktop", props={"cursor": "PointingHandCursor"})

@web_component  
def WebApp():
    return ui.Button("Web", props={"onclick": "handleClick()"})

# After: Unified component
@component(web=True, desktop=True)
def UnifiedApp():
    platform = get_current_platform()
    
    if platform == 'web':
        props = {"onclick": "handleClick()"}
    else:
        props = {"cursor": "PointingHandCursor"}
    
    return ui.Button("Universal", props=props)
```

### Prop Standardization
```python
# Old inconsistent naming
props = {
    "backgroundColor": "#fff",  # camelCase
    "font_size": "16px",        # snake_case
    "border-radius": "5px"      # kebab-case
}

# New standardized naming (kebab-case preferred)
props = {
    "background-color": "#fff",
    "font-size": "16px", 
    "border-radius": "5px"
}
```
