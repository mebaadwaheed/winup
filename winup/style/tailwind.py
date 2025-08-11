# Shared base styles for web (desktop will get converted)
BASE_CLASSES_WEB = {
    'bg-blue-500': {'background-color': '#3B82F6'},
    'text-black': {'color': '#000000'},
    'text-white': {'color': '#FFFFFF'},
    'w-1/2': {'width': '50%'},
    "text-xl": {'font-size': '1.25rem', 'line-height': '1.75rem'},
    "text-lg": {'font-size': '1.125rem', 'line-height': '1.75rem'},
    "text-sm": {'font-size': '0.875rem', 'line-height': '1.25rem'},
    "text-base": {'font-size': '1rem', 'line-height': '1.5rem'},
    "text-xs": {'font-size': '0.75rem', 'line-height': '1rem'},
    "font-bold": {'font-weight': 'bold'},
    "font-medium": {'font-weight': '500'},
    "font-light": {'font-weight': '300'},
}

# rem → px conversion for desktop (16px base)
REM_TO_PX = {
    "1.25rem": "20px",
    "1.75rem": "28px",
    "1.125rem": "18px",
    "0.875rem": "14px",
    "1rem": "16px",
    "1.5rem": "24px",
    "0.75rem": "12px",
}

# Build desktop base styles by replacing rem with px
BASE_CLASSES_DESKTOP = {}
for cls, styles in BASE_CLASSES_WEB.items():
    converted = {}
    for k, v in styles.items():
        if isinstance(v, str) and v.endswith("rem"):
            converted[k] = REM_TO_PX.get(v, v)  # convert if in map
        else:
            converted[k] = v
    BASE_CLASSES_DESKTOP[cls] = converted

# Units for padding & margin
SCALE_UNITS = {
    "desktop": {
        'p-4': {'padding': '16px'},
        'p-2': {'padding': '8px'},
        'p-1': {'padding': '4px'},
        'p-0': {'padding': '0px'},
        'm-4': {'margin': '16px'},
        'm-2': {'margin': '8px'},
        'm-1': {'margin': '4px'},
        'm-0': {'margin': '0px'},
    },
    "web": {
        'p-4': {'padding': '1rem'},
        'p-2': {'padding': '0.5rem'},
        'p-1': {'padding': '0.25rem'},
        'p-0': {'padding': '0rem'},
        'm-4': {'margin': '1rem'},
        'm-2': {'margin': '0.5rem'},
        'm-1': {'margin': '0.25rem'},
        'm-0': {'margin': '0rem'},
    }
}

# Merge into platform mappings
TAILWIND_TO_STYLE = {
    "desktop": {**BASE_CLASSES_DESKTOP, **SCALE_UNITS["desktop"]},
    "web": {**BASE_CLASSES_WEB, **SCALE_UNITS["web"]},
}


def transpile_tailwind(tailwind_string: str, platform: str = 'desktop'):
    """
    Transpiles a Tailwind CSS string to a dictionary of styles.

    Args:
        tailwind_string: A string of Tailwind CSS classes (e.g., "bg-blue-500 text-white").
        platform: The target platform ('desktop' for PySide6 QSS or 'web' for CSS).

    Returns:
        A dictionary of style properties.
    """
    style_dict = {}
    classes = tailwind_string.split()

    mappings = TAILWIND_TO_STYLE.get(platform, {})

    for cls in classes:
        if cls in mappings:
            style_dict.update(mappings[cls])

    return style_dict
