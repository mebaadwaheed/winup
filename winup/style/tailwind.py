# winup/style/tailwind.py

def transpile_tailwind(tailwind_string: str, platform: str = 'desktop'):
    """
    Transpiles a Tailwind CSS string to a dictionary of styles.

    Args:
        tailwind_string: A string of Tailwind CSS classes (e.g., "bg-blue-500 text-white").
        platform: The target platform ('desktop' for PySide6 QSS or 'web' for CSS).

    Returns:
        A dictionary of style properties.
    """
    # This is a placeholder implementation. I will expand this with more classes.
    style_dict = {}
    classes = tailwind_string.split()

    # Example mappings
    tailwind_to_style = {
        'desktop': {
            'bg-blue-500': {'background-color': '#3B82F6'},
            'text-black': {'color': '#000000'},
            'text-white': {'color': '#FFFFFF'},
            'p-4': {'padding': '16px'},
            'p-2': {'padding': '8px'},
            'p-1': {'padding': '4px'},
            'p-0': {'padding': '0px'},
            'm-4': {'margin': '16px'},
            'm-2': {'margin': '8px'},
            'm-1': {'margin': '4px'},
            'm-0': {'margin': '0px'},
            'w-1/2': {'width': '50%'},
        },
        'web': {
            'bg-blue-500': {'background-color': '#3B82F6'},
            'text-black': {'color': '#000000'},
            'text-white': {'color': '#FFFFFF'},
            'p-4': {'padding': '1rem'},
            'p-2': {'padding': '0.5rem'},
            'p-1': {'padding': '0.25rem'},
            'p-0': {'padding': '0rem'},
            'm-4': {'margin': '1rem'},
            'm-2': {'margin': '0.5rem'},
            'm-1': {'margin': '0.25rem'},
            'm-0': {'margin': '0rem'},
            'w-1/2': {'width': '50%'},
        }
    }

    mappings = tailwind_to_style.get(platform, {})

    for cls in classes:
        if cls in mappings:
            style_dict.update(mappings[cls])

    return style_dict
