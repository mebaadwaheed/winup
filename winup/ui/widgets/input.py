# winup/ui/input.py
import re
from typing import Union, Callable, Optional
from PySide6.QtWidgets import QLineEdit
from ... import style
from ...state import state as global_state

# Pre-compiled regex for common validation types
VALIDATION_PATTERNS = {
    "email": re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    "integer": re.compile(r"^-?\d+$"),
    "decimal": re.compile(r"^-?\d+(\.\d+)?$"),
}

class Input(QLineEdit):
    def __init__(self, placeholder="", text="", props=None, validation=None, on_submit: Optional[Callable] = None, on_text_changed: Optional[Callable] = None, **kwargs):
        super().__init__()
        
        # --- Prop Consolidation ---
        if props is None:
            props = {}
        # Merge kwargs into props for a single source of truth
        props.update(kwargs)

        # --- Extract Widget-Specific Properties from Props ---
        # Allow passing these as direct args or inside the props dict
        placeholder_text = props.pop('placeholder', placeholder)
        self.validation_rule = props.pop('validation', validation)
        initial_text = props.pop('text', text)
        
        # --- Event Handlers ---
        # These can also be passed in props or as direct args
        submit_handler = props.pop('on_submit', on_submit)
        text_changed_handler = props.pop('on_text_changed', on_text_changed)

        # --- Initial Setup ---
        if placeholder_text:
            self.setPlaceholderText(placeholder_text)
        if initial_text:
            self.setText(initial_text)
            
        self.textChanged.connect(self._on_text_changed)
        
        # Connect the custom text changed handler if provided
        if text_changed_handler:
            self.textChanged.connect(text_changed_handler)
        
        if submit_handler:
            self.returnPressed.connect(submit_handler)

        # Apply any remaining props as styles
        if props:
            style.apply_props(self, props)
        
        # Initial validation check
        self._on_text_changed(self.text())

    def _validate(self, text: str):
        """Internal method to check text against the validation rule."""
        is_valid = False
        if self.validation_rule is None:
            # If no rule, it's neither valid nor invalid
            style.styler.toggle_class(self, "valid", False)
            style.styler.toggle_class(self, "invalid", False)
            return

        if isinstance(self.validation_rule, str) and self.validation_rule in VALIDATION_PATTERNS:
            is_valid = bool(VALIDATION_PATTERNS[self.validation_rule].match(text))
        elif isinstance(self.validation_rule, re.Pattern):
            is_valid = bool(self.validation_rule.match(text))
        elif callable(self.validation_rule):
            is_valid = self.validation_rule(text)
        
        # Use the styler to toggle classes
        style.styler.toggle_class(self, "valid", is_valid)
        style.styler.toggle_class(self, "invalid", not is_valid)

    def _on_text_changed(self, text: str):
        self._validate(text)

    def set_text(self, text: str):
        """A more Pythonic alias for setText()."""
        self.setText(text)
        
    def get_text(self) -> str:
        """A more Pythonic alias for text()."""
        return self.text()
        
    def clear(self):
        """Clears the text from the input field."""
        self.setText("")