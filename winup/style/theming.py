# winup/style/theming.py
from typing import Dict, Optional

# Default Light Theme
LIGHT_THEME = {
    "primary-color": "#0078D4",
    "primary-text-color": "#FFFFFF",
    "secondary-color": "#EFEFEF",
    "secondary-text-color": "#000000",
    "background-color": "#FFFFFF",
    "text-color": "#212121",
    "border-color": "#CCCCCC",
    "hover-color": "#F0F0F0",
    "disabled-color": "#A0A0A0",
    "error-color": "#D32F2F",
}

# Default Dark Theme
DARK_THEME = {
    "primary-color": "#0096FF",
    "primary-text-color": "#FFFFFF",
    "secondary-color": "#3A3A3A",
    "secondary-text-color": "#FFFFFF",
    "background-color": "#212121",
    "text-color": "#F5F5F5",
    "border-color": "#505050",
    "hover-color": "#4A4A4A",
    "disabled-color": "#707070",
    "error-color": "#EF5350",
}

# Default styles for base Qt widgets that WinUp components use.
# These use theme variables so they adapt automatically.
DEFAULT_WIDGET_STYLES = {
    "QMainWindow": {
        "background-color": "$background-color",
    },
    "QLabel": {
        "color": "$text-color",
    },
    "QListWidget": {
        "background-color": "$secondary-color",
        "color": "$secondary-text-color",
        "border": "1px solid $border-color",
        "border-radius": "4px",
    },
    "QTreeWidget": {
        "background-color": "$secondary-color",
        "color": "$secondary-text-color",
        "border": "1px solid $border-color",
        "border-radius": "4px",
    },
    "QTreeView::item:selected": {
        "background-color": "$primary-color",
        "color": "$primary-text-color",
    },
    "QPushButton": {
        "background-color": "$secondary-color",
        "color": "$secondary-text-color",
        "border": "1px solid $border-color",
        "padding": "5px 10px",
        "border-radius": "4px",
    },
    "QPushButton:hover": {
        "background-color": "$hover-color",
    },
    "QColorDialog": {
        "background-color": "$background-color",
    }
}

class ThemeManager:
    """Manages application-wide themes and variable substitution."""
    
    def __init__(self, styler_instance):
        self._styler = styler_instance
        self._themes = {
            "light": LIGHT_THEME,
            "dark": DARK_THEME,
        }
        self._active_theme_name = "light"
        self._active_theme = self._themes["light"]

    def add_theme(self, name: str, theme_dict: Dict[str, str]):
        """Adds a new theme definition."""
        self._themes[name] = theme_dict
        print(f"Theme '{name}' added.")

    def set_theme(self, name: str, _force_reapply: bool = True):
        """Sets the active theme for the application and triggers a global restyle."""
        if name not in self._themes:
            raise ValueError(f"Theme '{name}' not found. Available themes: {list(self._themes.keys())}")
        
        # Avoid reapplying if the theme is already active and not forced
        if name == self._active_theme_name and not _force_reapply:
            return
            
        print(f"Switching to theme: {name}")
        self._active_theme_name = name
        self._active_theme = self._themes[name]
        
        # Trigger a global restyle only if requested
        if _force_reapply:
            self._styler.reapply_global_styles()

    def get_active_theme_name(self) -> str:
        """Returns the name of the currently active theme."""
        return self._active_theme_name

    def get_available_themes(self) -> list[str]:
        """Returns a list of the names of all available themes."""
        return list(self._themes.keys())

    def get_variable(self, name: str) -> Optional[str]:
        """Gets a variable's value from the active theme."""
        # Variables are denoted by a '$' prefix, e.g., '$primary-color'
        return self._active_theme.get(name.lstrip('$'))

    def substitute_variables(self, style_dict: Dict) -> Dict:
        """
        Recursively substitutes all theme variables in a style dictionary.
        This now correctly handles embedded variables (e.g., "1px solid $border-color").
        """
        substituted_dict = {}
        for key, value in style_dict.items():
            if isinstance(value, str):
                # Iterate through all theme variables and replace them in the string.
                # This is more robust than a simple startswith() check.
                new_value = value
                for var_name, var_value in self._active_theme.items():
                    new_value = new_value.replace(f'${var_name}', var_value)
                substituted_dict[key] = new_value
            elif isinstance(value, dict):
                # Recurse for nested dictionaries (e.g., hover states)
                substituted_dict[key] = self.substitute_variables(value)
            else:
                substituted_dict[key] = value
        return substituted_dict

# A singleton instance will be created in the style package __init__.py
theme_manager = None 