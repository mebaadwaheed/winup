import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QFont
# Import the class, not the module, to avoid the cycle
from .theming import ThemeManager

# --- Style Constants ---
# Provide framework-level access to common Qt constants to avoid direct Qt imports in user code.
AlignLeft = Qt.AlignmentFlag.AlignLeft
AlignRight = Qt.AlignmentFlag.AlignRight
AlignCenter = Qt.AlignmentFlag.AlignCenter
AlignTop = Qt.AlignmentFlag.AlignTop
AlignBottom = Qt.AlignmentFlag.AlignBottom
AlignVCenter = Qt.AlignmentFlag.AlignVCenter

# --- Cursor Constants ---
# Map string names to Qt.CursorShape enums for easier use in props.
CURSOR_MAP = {
    "ArrowCursor": Qt.CursorShape.ArrowCursor,
    "UpArrowCursor": Qt.CursorShape.UpArrowCursor,
    "CrossCursor": Qt.CursorShape.CrossCursor,
    "WaitCursor": Qt.CursorShape.WaitCursor,
    "IBeamCursor": Qt.CursorShape.IBeamCursor,
    "SizeVerCursor": Qt.CursorShape.SizeVerCursor,
    "SizeHorCursor": Qt.CursorShape.SizeHorCursor,
    "SizeBDiagCursor": Qt.CursorShape.SizeBDiagCursor,
    "SizeFDiagCursor": Qt.CursorShape.SizeFDiagCursor,
    "SizeAllCursor": Qt.CursorShape.SizeAllCursor,
    "BlankCursor": Qt.CursorShape.BlankCursor,
    "SplitVCursor": Qt.CursorShape.SplitVCursor,
    "SplitHCursor": Qt.CursorShape.SplitHCursor,
    "PointingHandCursor": Qt.CursorShape.PointingHandCursor,
    "ForbiddenCursor": Qt.CursorShape.ForbiddenCursor,
    "WhatsThisCursor": Qt.CursorShape.WhatsThisCursor,
    "BusyCursor": Qt.CursorShape.BusyCursor,
    "OpenHandCursor": Qt.CursorShape.OpenHandCursor,
    "ClosedHandCursor": Qt.CursorShape.ClosedHandCursor,
}

# Map for font weights
FONT_WEIGHT_MAP = {
    "thin": QFont.Weight.Thin,
    "extralight": QFont.Weight.ExtraLight,
    "light": QFont.Weight.Light,
    "normal": QFont.Weight.Normal,
    "medium": QFont.Weight.Medium,
    "demibold": QFont.Weight.DemiBold,
    "bold": QFont.Weight.Bold,
    "extrabold": QFont.Weight.ExtraBold,
    "black": QFont.Weight.Black,
}

def merge_props(default_props: dict, new_props: dict) -> dict:
    """
    Merges two dictionaries of props.
    Classes are combined, and other properties from new_props override default_props.
    """
    merged = default_props.copy()
    
    # Combine classes
    default_class = default_props.get("class", "")
    new_class = new_props.get("class", "")
    merged["class"] = f"{default_class} {new_class}".strip()
    
    # Update with new props, letting new_props win
    merged.update(new_props)
    
    return merged

class Styler:
    def __init__(self):
        self._app: QApplication = None
        self._definitions = {}
        # The styler will create and own the theme manager.
        self.themes: ThemeManager = None
        self._styled_widgets = {}

    def init_app(self, app: QApplication):
        """
        Stores the application instance, creates the theme manager,
        and applies any styles that were defined before initialization.
        """
        import winup.style
        self._app = app
        if not self.themes:
            self.themes = ThemeManager(self)
            winup.style.themes = self.themes

        # This is the crucial change: If themes have been added but none
        # is active, activate the first one as the default.
        if self.themes._themes and not self.themes._active_theme_name:
            first_theme = next(iter(self.themes._themes))
            self.themes.set_theme(first_theme, _force_reapply=False)

        if self._definitions:
            self.reapply_global_styles()

    def add_style_dict(self, styles: dict):
        """
        Adds a dictionary of styles to the application.
        The dictionary is converted to a QSS string and applied globally.
        """
        for selector, rules in styles.items():
            if selector not in self._definitions:
                self._definitions[selector] = {}
            self._definitions[selector].update(rules)
        
        # Only reapply styles if the application is already running.
        # Otherwise, init_app will handle it.
        if self._app:
            self.reapply_global_styles()

    def reapply_global_styles(self):
        """
        Substitutes theme variables in all defined styles and reapplies
        the global stylesheet.
        """
        if not self._app:
            return
            
        themed_styles = self.themes.substitute_variables(self._definitions)
        qss = self._to_qss(themed_styles)
        self._app.setStyleSheet(qss)

    def add_style(self, widget, style_class: str):
        """
        Applies a style class to a widget. This allows targeting widgets
        with QSS property selectors, e.g., `[class~="primary"]`.
        """
        current_classes = widget.property("class") or ""
        # Avoid adding duplicate classes
        if style_class not in current_classes.split():
            new_classes = f"{current_classes} {style_class}".strip()
            widget.setProperty("class", new_classes)
            self.repolish(widget)

    def set_id(self, widget, id_name: str):
        """Sets the object name for a widget, allowing it to be targeted with an ID selector."""
        widget.setObjectName(id_name)
        self.repolish(widget)

    def set_fixed_size(self, widget: QWidget, horizontal: bool = True, vertical: bool = True):
        """
        Prevents a widget from stretching during layout.

        Args:
            widget: The widget to modify.
            horizontal: If True, the widget will not stretch horizontally.
            vertical: If True, the widget will not stretch vertically.
        """
        policy = widget.sizePolicy()
        
        h_policy = QSizePolicy.Policy.Fixed if horizontal else QSizePolicy.Policy.Preferred
        v_policy = QSizePolicy.Policy.Fixed if vertical else QSizePolicy.Policy.Preferred
        
        policy.setHorizontalPolicy(h_policy)
        policy.setVerticalPolicy(v_policy)
        
        widget.setSizePolicy(policy)

    def toggle_class(self, widget: QWidget, class_name: str, condition: bool):
        """
        Adds or removes a class from a widget based on a condition.
        This is the recommended way to toggle styles dynamically.
        """
        current_classes = (widget.property("class") or "").split()
        
        # Add or remove the class based on the condition
        if condition and class_name not in current_classes:
            current_classes.append(class_name)
        elif not condition and class_name in current_classes:
            current_classes.remove(class_name)
            
        widget.setProperty("class", " ".join(current_classes))
        self.repolish(widget)

    def _to_qss(self, styles: dict) -> str:
        """Converts a style dictionary to a QSS string."""
        parts = []
        for selector, rules in styles.items():
            rules_str = "; ".join(f"{prop}: {val}" for prop, val in rules.items())
            parts.append(f"{selector} {{ {rules_str}; }}")
        return "\n".join(parts)

    def repolish(self, widget):
        """Triggers a style re-computation for the widget."""
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def apply_props(self, widget, props: dict):
        """Applies a dictionary of properties to a widget."""
        if not self._app and QApplication.instance():
            self.init_app(QApplication.instance())

        themed_props = self.themes.substitute_variables(props) if props else {}

        # Handle special properties first
        if "class" in themed_props:
            self.add_style(widget, themed_props.pop("class"))
        if "id" in themed_props:
            self.set_id(widget, themed_props.pop("id"))
        if "objectName" in themed_props:
            # objectName is an alias for id, used for QSS selectors
            self.set_id(widget, themed_props.pop("objectName"))
        if "cursor" in themed_props:
            cursor_name = themed_props.pop("cursor")
            cursor_shape = CURSOR_MAP.get(cursor_name)
            if cursor_shape:
                widget.setCursor(QCursor(cursor_shape))
            else:
                print(f"Warning: Unknown cursor name '{cursor_name}'.", file=sys.stderr)
        if "placeholder-text" in themed_props:
            if hasattr(widget, 'setPlaceholderText'):
                widget.setPlaceholderText(themed_props.pop("placeholder-text"))
            else:
                # Remove it anyway so it doesn't become invalid QSS
                themed_props.pop("placeholder-text")
                print(f"Warning: 'placeholder-text' prop used on a widget that doesn't support it.", file=sys.stderr)
        if "font-weight" in themed_props:
            weight_name = themed_props.pop("font-weight")
            font = widget.font()
            weight = FONT_WEIGHT_MAP.get(str(weight_name).lower())
            if weight:
                font.setWeight(weight)
                widget.setFont(font)
            else:
                print(f"Warning: Unknown font-weight '{weight_name}'.", file=sys.stderr)
        
        if "read-only" in themed_props:
            if hasattr(widget, 'setReadOnly'):
                is_read_only = themed_props.pop("read-only")
                # Ensure the value is a boolean
                widget.setReadOnly(bool(is_read_only))
            else:
                # Remove it anyway so it doesn't become invalid QSS
                themed_props.pop("read-only")
                print(f"Warning: 'read-only' prop used on a widget that doesn't support it.", file=sys.stderr)

        # The rest of the props are assumed to be direct CSS properties
        style_str = ""
        for key, value in themed_props.items():
            css_key = key.replace('_', '-')
            style_str += f"{css_key}: {value};"

        if style_str:
            existing_style = widget.styleSheet() or ""
            if existing_style and not existing_style.endswith(';'):
                existing_style += ';'
            widget.setStyleSheet(existing_style + " " + style_str)

# Singleton instance
styler = Styler() 