from typing import Dict, Any, Optional

def props_to_html(props: Optional[Dict[str, Any]]) -> str:
    """
    Converts a component's props dictionary into a string of HTML attributes.
    """
    if not props:
        return ""
    
    parts = []
    for key, value in props.items():
        if key.startswith('on') and isinstance(value, str):
            # For event handlers, the value is JS code, so wrap it.
            parts.append(f'{key}="{value}"')
        elif key == "style" and isinstance(value, dict):
            # Convert snake_case to kebab-case for CSS properties
            style_str = "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in value.items())
            parts.append(f'style="{style_str}"')
        elif key == "class_": 
            parts.append(f'class="{value}"')
        elif value is False:
            continue # Don't render attributes that are False (e.g., disabled=False)
        elif value is True:
            parts.append(key) # Render boolean attributes like "disabled"
        else:
            html_key = key.replace('_', '-')
            parts.append(f'{html_key}="{value}"')
            
    return " " + " ".join(parts) if parts else "" 