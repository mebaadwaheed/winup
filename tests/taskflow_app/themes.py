from winup import style

def apply_base_theme():
    """
    Applies a consistent and modern stylesheet for the TaskFlow application.
    This uses theme variables, so it works with the theme switcher.
    """
    # Define the variables for both themes first
    style.themes.add_theme("light", {
        "primary-color": "#007BFF",
        "primary-text-color": "#FFFFFF",
        "background-color": "#F8F9FA",
        "secondary-color": "#FFFFFF",
        "secondary-text-color": "#212529",
        "text-color": "#212529",
        "muted-text-color": "#6C757D",
        "border-color": "#DEE2E6",
        "hover-color": "#0056b3",
        "disabled-color": "#A0A0A0",
        "error-color": "#DC3545",
    })

    style.themes.add_theme("dark", {
        "primary-color": "#007BFF",
        "primary-text-color": "#FFFFFF",
        "background-color": "#212529",
        "secondary-color": "#2C3034",
        "secondary-text-color": "#F8F9FA",
        "text-color": "#F8F9FA",
        "muted-text-color": "#6C757D",
        "border-color": "#495057",
        "hover-color": "#0056b3",
        "disabled-color": "#707070",
        "error-color": "#E06C75",
    })
    
    # Set the default theme
    style.themes.set_theme("light")

    # Now, define the single, unified stylesheet using those variables
    style.add_style_dict({
        # --- Global & Typography ---
        "QMainWindow": {
            "background-color": "$background-color",
            "font-family": "Segoe UI, Arial, sans-serif",
        },
        "QLabel": {
            "color": "$text-color",
            "font-size": "14px",
        },
        ".h1": {
            "font-size": "20px",
            "font-weight": "bold",
            "color": "$text-color",
            "margin-bottom": "10px",
        },
        
        # --- Page & Main Layout ---
        "#main-window, #page-container": {
            "background-color": "$background-color",
        },
        "#page-container": {
            "padding": "0px 15px 15px 15px",
        },

        # --- Navbar ---
        "#navbar": {
            "background-color": "transparent",
            "padding": "0 15px",
            "border-bottom": "1px solid $border-color",
            "margin-bottom": "15px",
        },
        "#navbar .brand": {
            "font-size": "18px",
            "font-weight": "bold",
            "color": "$primary-color",
        },
        "#navbar QPushButton": {
            "background-color": "transparent",
            "color": "$text-color",
            "border": "none",
            "font-size": "14px",
            "font-weight": "500",
            "padding": "10px 0",
            "margin": "0 10px",
            "border-bottom": "2px solid transparent",
        },
        "#navbar QPushButton:hover": {
            "color": "$primary-color",
        },
        "#navbar .active": {
            "color": "$primary-color",
            "border-bottom-color": "$primary-color",
        },

        # --- Add Task Form ---
        "#add-task-form": {
            "margin-bottom": "15px",
        },
        "QLineEdit#add-task-input": {
            "border": "1px solid $border-color",
            "border-radius": "6px",
            "padding": "8px 12px",
            "font-size": "14px",
            "background-color": "$secondary-color",
            "color": "$text-color",
        },
        "QLineEdit#add-task-input:focus": {
            "border-color": "$primary-color",
        },
        ".add-button": {
            "background-color": "$primary-color",
            "color": "$primary-text-color",
            "border": "none",
            "border-radius": "6px",
            "font-weight": "bold",
            "padding": "8px 20px",
        },
        ".add-button:hover": {
            "background-color": "$hover-color",
        },

        # --- Task List & Items ---
        "#task-list-container": {
            "spacing": "8px",
        },
        ".task-item, .task-item-completed": {
            "background-color": "$secondary-color",
            "border-radius": "6px",
            "padding": "12px",
            "border": "1px solid $border-color",
        },
        ".task-title": {
            "font-size": "15px",
        },
        ".task-item-completed .task-title": {
            "text-decoration": "line-through",
            "color": "$muted-text-color",
        },
        ".delete-btn": {
            "background-color": "transparent",
            "color": "$muted-text-color",
            "border": "none",
            "padding": "5px",
            "font-weight": "bold",
            "font-size": "16px",
            "border-radius": "4px",
        },
        ".delete-btn:hover": {
            "color": "$error-color",
            "background-color": "rgba(220, 53, 69, 0.1)",
        },
        
        # --- Settings Page ---
        ".settings-page .h1": {
            "margin-bottom": "20px",
        },
        ".theme-switcher": {
            "spacing": "10px",
        },

        # --- General Widgets ---
        "QSwitch::indicator:checked": {
            "background-color": "$primary-color",
        }
    })

# Universal styles that apply to both themes
base_styles = {
    "QMainWindow": {
        "font-family": "Segoe UI"
    },
    "QPushButton": {
        "padding": "8px 15px",
        "border-radius": "4px",
        "font-size": "14px",
        "border": "1px solid transparent"
    },
    "QLabel": {
        "font-size": "14px"
    },
    "QLineEdit": {
        "padding": "8px",
        "border-radius": "4px",
        "font-size": "14px",
        "border": "1px solid"
    },
    "#navbar": {
        "background-color": "transparent",
        "border-bottom": "1px solid",
    },
    "#navbar QPushButton": {
        "border": "none",
        "padding": "10px",
        "font-weight": "bold",
        "border-bottom": "2px solid transparent",
    },
    "#navbar QPushButton[class~='active']": {
        "border-bottom-color": "#007BFF"
    },
    "Frame[class~='card']": {
        "border-radius": "6px",
        "border": "1px solid",
    },
    "QLineEdit[class~='valid']": {
        "border-color": "#28a745"
    },
    "QLineEdit[class~='invalid']": {
        "border-color": "#dc3545"
    }
}

light_theme = {
    **base_styles,
    "QMainWindow": {
        **base_styles["QMainWindow"],
        "background-color": "#ffffff",
    },
    "QLabel": {
        **base_styles["QLabel"],
        "color": "#212529"
    },
    "QLineEdit": {
        **base_styles["QLineEdit"],
        "border-color": "#ced4da",
        "background-color": "#ffffff",
        "color": "#495057"
    },
    "QPushButton": {
        **base_styles["QPushButton"],
        "background-color": "#f8f9fa",
        "color": "#343a40",
        "border-color": "#ced4da"
    },
    "QPushButton[class~='primary']": {
        "background-color": "#007bff",
        "color": "white",
        "border-color": "#007bff"
    },
    "#navbar": {
        **base_styles["#navbar"],
        "border-bottom-color": "#dee2e6"
    },
    "Frame[class~='card']": {
        **base_styles["Frame[class~='card']"],
        "border-color": "#dee2e6",
        "background-color": "#f8f9fa"
    }
}

dark_theme = {
    **base_styles,
    "QMainWindow": {
        **base_styles["QMainWindow"],
        "background-color": "#212529",
    },
    "QLabel": {
        **base_styles["QLabel"],
        "color": "#f8f9fa"
    },
    "QLineEdit": {
        **base_styles["QLineEdit"],
        "border-color": "#495057",
        "background-color": "#343a40",
        "color": "#f8f9fa"
    },
    "QPushButton": {
        **base_styles["QPushButton"],
        "background-color": "#343a40",
        "color": "#f8f9fa",
        "border-color": "#495057"
    },
    "QPushButton[class~='primary']": {
        "background-color": "#007bff",
        "color": "white",
        "border-color": "#007bff"
    },
    "#navbar": {
        **base_styles["#navbar"],
        "border-bottom-color": "#343a40"
    },
    "Frame[class~='card']": {
        **base_styles["Frame[class~='card']"],
        "border-color": "#495057",
        "background-color": "#343a40"
    }
} 