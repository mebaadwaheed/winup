"""
The UI module for WinUp.

This package exposes all the available UI widgets, layouts, and dialogs
through a factory system to allow for custom widget implementations.
"""
from .widget_factory import register_widget, create_widget, create_component
from .layouts import VBox, HBox
from .utils import clear_layout
from winup.style.styler import merge_props
from winup.core.memoize import memo

# Dialogs
from . import dialogs

# --- Public API ---
# These are factory functions, not classes. They create widgets from the registry.
# This makes the API user-friendly, e.g., ui.Button("Click me").

def Button(*args, **kwargs): return create_widget("Button", *args, **kwargs)
def Calendar(*args, **kwargs): return create_widget("Calendar", *args, **kwargs)
def Checkbox(*args, **kwargs): return create_widget("Checkbox", *args, **kwargs)
def ComboBox(*args, **kwargs): return create_widget("ComboBox", *args, **kwargs)
def Deck(*args, **kwargs): return create_widget("Deck", *args, **kwargs)
@memo
def Frame(*args, **kwargs): return create_widget("Frame", *args, **kwargs)
@memo
def Image(*args, **kwargs): return create_widget("Image", *args, **kwargs)
def Input(*args, **kwargs): return create_widget("Input", *args, **kwargs)
@memo
def Label(*args, **kwargs): return create_widget("Label", *args, **kwargs)
@memo
def Link(*args, **kwargs): return create_widget("Link", *args, **kwargs)
def ProgressBar(*args, **kwargs): return create_widget("ProgressBar", *args, **kwargs)
def RadioButton(*args, **kwargs): return create_widget("RadioButton", *args, **kwargs)
def ScrollView(*args, **kwargs): return create_widget("ScrollView", *args, **kwargs)
def Slider(*args, **kwargs): return create_widget("Slider", *args, **kwargs)
def Switch(*args, **kwargs): return create_widget("Switch", *args, **kwargs)
def TabView(*args, **kwargs): return create_widget("TabView", *args, **kwargs)
def Textarea(*args, **kwargs): return create_widget("Textarea", *args, **kwargs)
def Carousel(*args, **kwargs): return create_widget("Carousel", *args, **kwargs)
def ExpandablePanel(*args, **kwargs): return create_widget("ExpandablePanel", *args, **kwargs)

# Layouts
def Column(*args, **kwargs): return create_widget("Column", *args, **kwargs)
def Row(*args, **kwargs): return create_widget("Row", *args, **kwargs)
def Stack(*args, **kwargs): return create_widget("Stack", *args, **kwargs)
def Grid(*args, **kwargs): return create_widget("Grid", *args, **kwargs)

# Graphing Widgets
def BarChart(*args, **kwargs): return create_widget("BarChart", *args, **kwargs)
def LineChart(*args, **kwargs): return create_widget("LineChart", *args, **kwargs)
def PieChart(*args, **kwargs): return create_widget("PieChart", *args, **kwargs)
def ScatterPlot(*args, **kwargs): return create_widget("ScatterPlot", *args, **kwargs)


# Expose all factory functions and the registration function for discoverability.
__all__ = [
    "register_widget",
    "create_component",
    "Button", "Calendar", "Checkbox", "ComboBox", "Deck", "Frame", "Image",
    "Input", "Label", "Link", "ProgressBar", "RadioButton", "ScrollView",
    "Slider", "Switch", "TabView", "Textarea",
    "Row", "Column", "Stack", "Grid",
    "BarChart", "LineChart", "PieChart", "ScatterPlot",
    "Carousel", "ExpandablePanel"
    "clear_layout", "dialogs", "VBox", "HBox", "merge_props"
] 