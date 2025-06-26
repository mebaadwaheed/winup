# Core Concepts

## UI & Layouts

WinUp abstracts away Qt's manual layout system. You build UIs by composing `Row` and `Column` components.

```python
def App():
    return ui.Column(  # Arranges children vertically
        children=[
            ui.Label("Top"),
            ui.Row(    # Arranges children horizontally
                children=[
                    ui.Button("Left"),
                    ui.Button("Right")
                ],
                props={"spacing": 10}
            ),
            ui.Label("Bottom")
        ],
        props={"spacing": 15, "margin": "20px"}
    )
```

## Advanced Layouts: Stack, Grid, and Stretch

Beyond simple `Row` and `Column`, WinUp provides more advanced layouts for building complex UIs.

**1. Stack Layout**

A `Stack` layout places its children on top of each other, like a deck of cards. Only one child is visible at a time. This is perfect for wizards, tab-less interfaces, or navigation with a `RouterView`.

```python
def App():
    # The main stack layout
    main_stack = ui.Stack(children=[
        ui.Label("Page 1"),
        ui.Label("Page 2"),
    ])

    # Controls to switch between pages
    return ui.Column(children=[
        main_stack,
        ui.Row(children=[
            ui.Button("Show Page 1", on_click=lambda: main_stack.set_current_index(0)),
            ui.Button("Show Page 2", on_click=lambda: main_stack.set_current_index(1)),
        ])
    ])
```

**2. Grid Layout**

For form fields, dashboards, or calculator-style interfaces, the `Grid` layout is ideal. You specify children as tuples containing the widget and its grid position: `(widget, row, col)`. You can also specify row and column spans: `(widget, row, col, row_span, col_span)`.

```python
def App():
    return ui.Grid(
        props={"spacing": 10},
        children=[
            # A 2x2 grid
            (ui.Button("Top-Left"), 0, 0),
            (ui.Button("Top-Right"), 0, 1),
            (ui.Button("Bottom-Left"), 1, 0),
            (ui.Button("Bottom-Right"), 1, 1),
            
            # A button spanning two columns
            (ui.Button("Full-Width Button"), 2, 0, 1, 2) # (widget, row, col, rowspan, colspan)
        ]
    )
```

**3. Row & Column Stretching (Flexbox-like)**

To create flexible UIs that adapt to window size, you can add a `stretch` factor to children of a `Row` or `Column`. This works like the `flex-grow` property in CSS. A child with a higher stretch factor will take up more available space.

In this example, the middle label (`stretch: 2`) will be twice as wide as the other two.

```python
def App():
    return ui.Row(
        props={"spacing": 5},
        children=[
            (ui.Label("Takes up 1 part"), {"stretch": 1}),
            (ui.Label("Takes up 2 parts"), {"stretch": 2}),
            (ui.Label("Takes up 1 part"), {"stretch": 1}),
        ]
    )
```

## Styling

You can style any widget by passing a `props` dictionary. Props can be CSS-like properties, or special keywords like `class` and `id` for use with a global stylesheet.

```python
# Define global styles
winup.style.add_style_dict({
    ".btn-primary": {
        "background-color": "#007bff",
        "color": "white",
        "border-radius": "5px",
        "padding": "10px"
    },
    ".btn-primary:hover": {
        "background-color": "#0056b3"
    }
})

# Use the class in a component
def App():
    return ui.Button("Primary Button", props={"class": "btn-primary"})
```

**Styling with an ID**

For targeting a single, specific widget, you can use the `id` prop. This is equivalent to an ID in HTML/CSS and is the most specific selector. In your stylesheet, you target it with a `#` prefix.

```python
# Add a style rule for a specific widget ID
winup.style.add_style_dict({
    "#special-button": {
        "border": "2px dashed #FF5722",
        "font-size": "16px"
    }
})

# Apply the ID to one specific instance
def App():
    return ui.Column(children=[
        ui.Button("Normal Button"),
        ui.Button("Special Button", props={"id": "special-button"})
    ])
```

## Theming and Dynamic Styling

WinUp includes a powerful theming system that lets you define and switch between different looks for your application (e.g., light and dark mode) at runtime.

The system is built on a simple concept: **theme variables**. You define your application's stylesheet using variables (like `$primary-color` or `$text-color`). Then, you can define multiple "themes" that provide concrete values for these variables.

**1. Using Theme Variables**

You can use theme variables in two places:
*   In a global stylesheet using `style.styler.add_style_dict()`.
*   Directly in a widget's `props` dictionary.

```python
# Define styles using variables
style.styler.add_style_dict({
    "QPushButton#action-button": {
        "background-color": "$primary-color",
        "color": "$primary-text-color",
        "font-weight": "bold",
    },
    "QLabel.title": {
        "color": "$text-color",
        "font-size": "24px",
    }
})

# Use variables directly in props
def App():
    return ui.Frame(
        props={"background-color": "$background-color"},
        children=[
            ui.Label("Hello Themed World!", props={"class": "title"}),
            ui.Button("Click Me", props={"id": "action-button"}),
        ]
    )
```

**2. Switching Themes**

WinUp comes with built-in `light` and `dark` themes. You can switch between them at any time using `style.styler.themes.set_theme()`.

```python
from winup import style

def toggle_theme():
    # Access the theme manager through the styler singleton
    current_theme = style.styler.themes._active_theme_name
    if current_theme == "light":
        style.styler.themes.set_theme("dark")
    else:
        style.styler.themes.set_theme("light")

# You can connect this function to a button click or a settings switch.
# The entire application will automatically restyle itself.
```

**3. Creating Custom Themes**

You can easily define your own themes by providing a dictionary of variable names to color values.

```python
from winup import style

# Define a custom "matrix" theme
matrix_theme = {
    "primary-color": "#00FF41",
    "primary-text-color": "#000000",
    "background-color": "#0D0208",
    "text-color": "#00FF41",
    "border-color": "#008F11",
    "hover-color": "#00A62A",
}

# Add it to the theme manager via the styler
style.styler.themes.add_theme("matrix", matrix_theme)

# Now you can switch to it
style.styler.themes.set_theme("matrix")
```

## Creating Reusable Components

While you can use raw `ui` elements everywhere, the best way to build a maintainable application is to create your own library of reusable components. WinUp provides two main ways to do this.

**1. Styled Variants (Recommended)**

This is the most common and powerful pattern. You can create a new, reusable component by wrapping a base widget with default `props`. This is perfect for creating a consistent design system (e.g., `PrimaryButton`, `SecondaryButton`, `Card`, `Avatar`).

The `ui.create_component` function is the key to this pattern.

```python
# components.py
from winup import ui

# Create a PrimaryButton variant with default styles
PrimaryButton = ui.create_component(
    ui.Button,
    {
        "class": "btn-primary", # Target with global stylesheet
        "padding": "10px 15px",
        "font-weight": "bold",
    }
)

# Create an AlertLabel variant
AlertLabel = ui.create_component(
    ui.Label,
    {
        "background-color": "$error-color",
        "color": "$primary-text-color",
        "padding": "10px",
        "border-radius": "4px",
    }
)

# --- In your main application ---
# from components import PrimaryButton, AlertLabel

def App():
    return ui.Column(children=[
        PrimaryButton("Click me!"),
        # You can still override props at the instance level
        PrimaryButton("Cancel", props={"background-color": "$disabled-color"}),
        AlertLabel("Something went wrong!"),
    ])
```

**2. Subclassing (For Advanced Behavior)**

If you need to add new *behavior* to a widget (not just styles), you can fall back to standard Python subclassing. This is useful for creating highly specialized components with their own internal logic. After creating your class, you can register it with `ui.register_widget` to make it available everywhere.

```python
from winup.ui.widgets.input import Input as DefaultInput

class PasswordInput(DefaultInput):
    """An Input that hides text by default but has a toggle button."""
    def __init__(self, props: dict = None):
        super().__init__(props=props)
        # In a real implementation, you would add a button here
        # and connect it to self.setEchoMode().
        self.setEchoMode(self.EchoMode.Password)

# In your main script, before winup.run():
# This makes `ui.PasswordInput()` available if you register it.
# ui.register_widget("PasswordInput", PasswordInput)
```

## Traits System: Adding Behavior without Subclassing

While subclassing is great for creating new *kinds* of widgets, sometimes you just want to add a small, reusable piece of behavior to an *existing* widget—like making it draggable or giving it a right-click menu. This is where Traits come in.

Traits are modular behaviors that can be dynamically attached to any widget instance. WinUp comes with several built-in traits:

*   `draggable` & `droptarget`: A powerful, data-driven system for drag-and-drop functionality.
*   `context_menu`: Adds a custom right-click context menu.
*   `tooltip`: A simple way to add a hover tooltip.
*   `hover_effect`: Applies a `[hover="true"]` style property on mouse-over, which you can target in your stylesheets (e.g., `QPushButton[hover="true"]`).
*   `highlightable`: Makes the text of a widget (like `ui.Label`) selectable by the user.

You can add a trait to any widget using `winup.traits.add_trait()`.

**Example: Advanced Drag-and-Drop**

The new drag-and-drop system is data-driven. You make a widget `draggable` and provide it with data. You make another widget a `droptarget` and tell it what kind of data it `accepts` and what to do `on_drop`.

```python
# dnd_demo.py
import winup
from winup import ui, traits, state

def App():
    # Use state to manage the lists
    state.create("list_a", [{"id": 1, "text": "Item A"}])
    state.create("list_b", [{"id": 2, "text": "Item B"}])

    def move_item(source_list_key, target_list_key, item_id):
        # Find the item and move it between the state lists
        source_list = state.get(source_list_key)
        item_to_move = next((item for item in source_list if item["id"] == item_id), None)
        
        if item_to_move:
            new_source = [i for i in source_list if i["id"] != item_id]
            state.set(source_list_key, new_source)
            state.set(target_list_key, state.get(target_list_key) + [item_to_move])

    # A reusable component for our drop zones
    @winup.component
    def DropList(title, list_key, accepts_type):
        list_container = ui.Column(props={"spacing": 5, "min-height": "100px", "background-color": "#f0f0f0", "padding": "10px"})
        
        # 1. Make the container a drop target
        traits.add_trait(list_container, "droptarget",
            accepts=[accepts_type],
            on_drop=lambda data: move_item(data["source_list"], list_key, data["item_id"])
        )

        def render_list(items):
            winup.core.hot_reload.clear_layout(list_container.layout())
            for item in items:
                # 2. Make each item draggable
                draggable_widget = ui.Label(item["text"], props={"padding": "8px", "background-color": "white"})
                traits.add_trait(draggable_widget, "draggable",
                    data={"type": accepts_type, "item_id": item["id"], "source_list": list_key}
                )
                list_container.add_child(draggable_widget)
        
        state.subscribe(list_key, render_list)
        render_list(state.get(list_key))
        return ui.Column([ui.Label(title, props={"font-weight": "bold"}), list_container])

    return ui.Row(props={"spacing": 20, "margin": "20px"}, children=[
        DropList("List A (drag from here)", "list_a", "list-item"),
        DropList("List B (drop here)", "list_b", "list-item"),
    ])

if __name__ == "__main__":
    winup.run(main_component_path="dnd_demo:App", title="Drag and Drop Demo")
```

## State Management: The Reactive Core

WinUp includes a powerful state management system that lets you create reactive UIs with minimal boilerplate. The new, recommended approach is object-oriented, making your code safer and more readable.

**The New Way: `state.create()` and `bind_to()` (Recommended)**

Instead of using string keys, you now create dedicated `State` objects. These objects are the single source of truth for your data and provide methods to interact with that data.

The real power comes from the `bind_to()` method, which can link one or more state objects to *any* widget property, using a simple function to format the final value.

**1. Simple Counter Example**

Here, we create a `counter` state object and bind it to a label's `text` property. The `lambda` function formats the output.

```python
# new_state_demo.py
import winup
from winup import ui

def App():
    # 1. Create a state object with an initial value.
    counter = winup.state.create("counter", 0)

    # 2. Create the UI widgets.
    label = ui.Label() 

    # 3. Bind the state to the label's 'text' property.
    # The lambda function will re-run whenever the counter changes.
    counter.bind_to(label, 'text', lambda c: f"Counter Value: {c}")

    def increment():
        # 4. Use the state object's methods to update the value.
        counter.set(counter.get() + 1)

    return ui.Column(children=[
        label,
        ui.Button("Increment", on_click=increment)
    ])

if __name__ == "__main__":
    winup.run(main_component_path="new_state_demo:App", title="New State Demo")
```

**2. Multi-State Binding**

Need a widget to react to changes in *multiple* state values? Use the `and_()` method to combine them. The formatter `lambda` will receive the state values as arguments in the same order.

```python
def App():
    # Create two state objects
    first_name = winup.state.create("first_name", "John")
    last_name = winup.state.create("last_name", "Doe")
    
    greeting_label = ui.Label()

    # Bind the label's text to BOTH state objects
    first_name.and_(last_name).bind_to(
        greeting_label,
        'text',
        lambda fn, ln: f"Full Name: {fn} {ln}"
    )

    # ... widgets to change first_name and last_name
```

**3. Two-Way Binding for Inputs**

For the common case of syncing an `Input` widget with a state, the `bind_two_way()` helper is still available. It works directly with the state key.

```python
email_input = ui.Input()
# The input's value updates the state, and the state updates the input's value.
winup.state.bind_two_way(email_input, 'email_value')
```

---
**Legacy State Management (Old API)**

For backward compatibility, the older, string-based API is still functional.

*   `winup.state.set("key", value)`: Sets a value in the global store.
*   `winup.state.get("key")`: Retrieves a value.
*   `winup.state.bind(widget, "property", "key")`: A simple one-way binding to a widget's property.
*   `winup.state.subscribe("key", callback)`: Calls a function whenever a value changes.

```python
# old_api_demo.py
winup.state.set("legacy_counter", 0)
label = ui.Label()
winup.state.bind(label, "text", "legacy_counter") # Binds to the text property

def increment():
    winup.state.set("legacy_counter", winup.state.get("legacy_counter") + 1)
```

## Asynchronous Task Runner (`@tasks.run`)

To keep your application responsive, any long-running operation (like a network request or a complex calculation) should be run on a background thread. WinUp makes this incredibly simple with the `@tasks.run` decorator.

It handles all the complex threading logic for you. You just need to provide callbacks for when the task starts, finishes, or encounters an error.

```python
from winup import tasks, shell
import time

# These callbacks will be executed safely on the main GUI thread.
def on_task_start():
    shell.StatusBar.show_message("Processing...", -1) # Show message indefinitely

def on_task_finish(result):
    print(f"Task finished with result: {result}")
    shell.StatusBar.show_message(f"Success: {result}", 5000) # Show for 5s

def on_task_error(error_details):
    exception, traceback_str = error_details
    print(f"Task failed: {exception}")
    shell.StatusBar.show_message(f"Error: {exception}", 5000)

# Decorate your long-running function
@tasks.run(on_start=on_task_start, on_finish=on_task_finish, on_error=on_task_error)
def fetch_data_from_server(url: str):
    """This function runs on a background thread."""
    print("Fetching data...")
    time.sleep(3) # Simulate a network request
    if "error" in url:
        raise ConnectionError("Could not connect to server.")
    return "Data fetched successfully!"

# In your UI, just call the function as you normally would.
# WinUp will automatically delegate it to the background thread pool.
def App():
    return ui.Row(children=[
        ui.Button("Fetch Data", on_click=lambda: fetch_data_from_server("my-api.com/data")),
        ui.Button("Trigger Error", on_click=lambda: fetch_data_from_server("my-api.com/error")),
    ])
```

The decorator accepts three optional callback arguments:
*   `on_start`: A function to call right before the task begins executing.
*   `on_finish`: A function that will receive the return value of your function if it completes successfully.
*   `on_error`: A function that will receive a `(exception, traceback)` tuple if your function raises an exception.

## Developer Tools

**Hot Reloading (React-style Fast Refresh):**
WinUp now features a fully automatic, intelligent hot reloading system. Simply run your application with `dev=True`, and the framework will automatically watch all of your project's Python files for changes.

When you save a file, WinUp will instantly reload the relevant parts of your code and re-render your UI without restarting the entire application, preserving your application's state. This provides a seamless development experience similar to modern web frameworks.

**How to Use:**
Just pass the `dev=True` flag to the `run` function. That's it!

```python
# my_app.py
import winup
from winup import ui

@winup.component
def App():
    # Change this text, save the file, and see the UI update instantly.
    return ui.Label("Hello, Hot Reloading!")

if __name__ == "__main__":
    # Run in development mode to enable hot reloading.
    winup.run(main_component_path="my_app:App", title="Hot Reload Demo", dev=True)
```
*This setup allows you to see UI changes instantly just by saving any file in your project.*

**Performance & Memoization:**
For UIs that render large amounts of data, you can significantly improve performance by caching component results. The `@winup.memo` decorator automatically caches the widget created by a component. If the component is called again with the same arguments, the cached widget is returned instantly instead of being re-created.

```python
import winup
from winup import ui

# By adding @winup.memo, this component will only be re-created
# if the 'color' argument changes.
@winup.memo
def ColorBlock(color: str):
    return ui.Frame(props={"background-color": color, "min-height": "20px"})

def App():
    # In this list, ColorBlock('#AABBCC') will only be called once.
    # The framework will then reuse the cached widget for the other two instances.
    return ui.Column(children=[
        ColorBlock(color="#AABBCC"),
        ColorBlock(color="#EEEEEE"),
        ColorBlock(color="#AABBCC"),
        ColorBlock(color="#AABBCC"),
    ])
```

**Profiler:**
Simply add the `@profiler.measure()` decorator to any function to measure its execution time. Results are printed to the console when the application closes.
The profiler also automatically tracks the performance of the memoization cache, showing you hits, misses, and the overall hit ratio.

```python
from winup.tools import profiler

@profiler.measure
def some_expensive_function():
    # ... code to measure ...
    import time
    time.sleep(1)
```

## Built-in Routing: Creating Multi-Page Applications

WinUp includes a simple yet powerful router that allows you to build applications with multiple pages or views, like a settings screen, a user dashboard, or different application tabs.

The system is built around three core concepts:

1.  **`Router`**: An object that holds your application's routes (a mapping of a path like `"/home"` to a component function) and manages the current state.
2.  **`RouterView`**: A special component that acts as a placeholder. It automatically displays the correct component for the current route.
3.  **`RouterLink`**: A clickable component (like a hyperlink) that tells the `Router` to navigate to a different path.

**Example: A Simple Multi-Page App**

Here's how you can structure a basic application with a "Home" and "Settings" page.

```python
# multi_page_app.py
import winup
from winup import ui
from winup.router import Router, RouterView, RouterLink

# 1. Define your page components
@winup.component
def HomePage():
    return ui.Label("Welcome to the Home Page!", props={"font-size": "18px"})

@winup.component
def SettingsPage():
    return ui.Column(children=[
        ui.Label("Settings", props={"font-size": "18px"}),
        ui.Switch(text="Enable Dark Mode")
    ])

# 2. Create a router instance with your routes
app_router = Router({
    "/": HomePage,
    "/settings": SettingsPage,
})

# 3. Build the main application layout
def App():
    return ui.Column(
        props={"spacing": 15, "margin": "10px"},
        children=[
            # Navigation links
            ui.Row(
                props={"spacing": 20},
                children=[
                    RouterLink(router=app_router, to="/", text="Home"),
                    RouterLink(router=app_router, to="/settings", text="Settings")
                ]
            ),
            # The RouterView will render either HomePage or SettingsPage
            ui.Frame(
                props={"border": "1px solid #ccc", "padding": "10px"},
                children=[
                    RouterView(router=app_router)
                ]
            )
        ]
    )

if __name__ == "__main__":
    # You need to create the router files first for this to work.
    winup.run(main_component_path="multi_page_app:App", title="Multi-Page App Demo")
```

**Nested Routing and Layouts**

For more complex applications, you often need nested views (e.g., an "Account" section with its own sub-navigation for "Profile" and "Billing"). The router supports this through a layout-based approach.

Instead of nesting `RouterView` components, the recommended pattern is to create a **layout component** that accepts a `child_view` function as a prop. Each route then renders the layout component, passing in the specific child page it should display.

This approach is more explicit, easier to reason about, and avoids potential recursion issues.

```python
# nested_routing_app.py
import winup
from winup import ui
from winup.router import Router, RouterView, RouterLink
from typing import Callable

# 1. Define the pages
@winup.component
def DetailsPage():
    return ui.Label("Your account details.")

@winup.component
def BillingPage():
    return ui.Label("Your billing information.")

# 2. Create the shared layout component
@winup.component
def AccountLayout(router: Router, child_view: Callable):
    """A layout that contains sub-navigation and renders a child view."""
    return ui.Column(props={"spacing": 10}, children=[
        ui.Label("Account Settings", props={"font-weight": "bold"}),
        ui.Row(children=[
            RouterLink(router, "/account/details", "Details"),
            RouterLink(router, "/account/billing", "Billing"),
        ]),
        # Render the specific child page here
        ui.Frame(props={"border": "1px solid #eee", "padding": "10px"}, children=[
            child_view()
        ])
    ])

# 3. Define the routes using the layout
app_router = Router({
    # Each route renders the layout with a different child
    "/account/details": lambda: AccountLayout(router=app_router, child_view=DetailsPage),
    "/account/billing": lambda: AccountLayout(router=app_router, child_view=BillingPage),
    # Add a redirect for the base path
    "/account": {"redirect": "/account/details"},
})
```

## Component Lifecycle Hooks: `on_mount` and `on_unmount`

To manage side effects—like fetching data, setting up timers, or starting animations—WinUp components now have lifecycle hooks. These are special functions you can pass to a component that run at specific times.

*   `on_mount`: This function is called exactly once, right after the component's UI has been created and added to the scene (i.e., it has "mounted"). It's the perfect place to load data or start animations.
*   `on_unmount`: This function is called exactly once, just before the component is destroyed and removed from the scene. It's essential for cleanup tasks, like canceling network requests, invalidating timers, or saving state.

**Example: A Self-Updating Clock**

This example demonstrates how to use `on_mount` to start a timer and `on_unmount` to clean it up, preventing memory leaks.

```python
# lifecycle_demo.py
import winup
from winup import ui, state
from PySide6.QtCore import QTimer

@winup.component
def Clock():
    # 1. A state to hold the current time string
    time_state = state.create("current_time", "Loading...")
    
    # 2. A variable to hold our QTimer instance
    timer = None

    def update_time():
        # This function will be called by the timer
        import datetime
        now = datetime.datetime.now()
        time_state.set(now.strftime("%H:%M:%S"))

    def on_mount():
        nonlocal timer
        print("Clock Mounted: Starting timer.")
        # Create and start the timer when the component appears
        timer = QTimer()
        timer.timeout.connect(update_time)
        timer.start(1000) # Update every 1000 ms (1 second)
        update_time() # Initial update

    def on_unmount():
        nonlocal timer
        print("Clock Unmounted: Stopping timer.")
        # Stop the timer when the component disappears to avoid errors
        if timer:
            timer.stop()
            timer = None

    # 3. Create a label and bind its text to our state
    time_label = ui.Label()
    time_state.bind_to(time_label, 'text', lambda t: f"Current Time: {t}")

    # 4. Pass the hooks to the component container
    return ui.Frame(
        children=[time_label],
        on_mount=on_mount,
        on_unmount=on_unmount
    )

# A simple app to show/hide the clock to test the hooks
def App():
    visibility_state = state.create("clock_visible", True)

    def toggle_clock():
        visibility_state.set(not visibility_state.get())

    placeholder = ui.Frame(props={"min-height": "50px"})
    
    def on_visibility_change(is_visible):
        clear_layout(placeholder.layout())
        if is_visible:
            placeholder.add_child(Clock())
        else:
            placeholder.add_child(ui.Label("Clock is hidden."))
            
    visibility_state.subscribe(on_visibility_change)
    on_visibility_change(visibility_state.get()) # Initial render

    return ui.Column(children=[
        ui.Button("Toggle Clock", on_click=toggle_clock),
        placeholder
    ])

if __name__ == "__main__":
    # You will need to import clear_layout from winup.core.hot_reload
    from winup.core.hot_reload import clear_layout 
    winup.run(main_component_path="lifecycle_demo:App", title="Lifecycle Demo")
```

## Built-in Animations & Effects

WinUp provides a simple API for creating smooth animations, located in the `winup.animate.fx` module. You can easily fade widgets in and out or animate any of their properties.

**Example: Fading and Moving**

This example shows how to use `fade_in`, `fade_out`, and the generic `animate` function to move a widget.

```python
# animation_demo.py
import winup
from winup import ui
from winup.animate import fx # Import the animation functions
from PySide6.QtCore import QRect

def App():
    
    animated_label = ui.Label(
        "Animate Me!",
        props={"padding": "20px", "background-color": "#ADD8E6"}
    )
    
    def slide_in():
        # Animate the widget's geometry (position and size)
        start_rect = animated_label.geometry()
        end_rect = QRect(20, 20, start_rect.width(), start_rect.height())
        fx.animate(animated_label, b"geometry", end_rect, 500)

    # Place the label in a container with a null layout for manual positioning
    container = ui.Frame(
        props={"layout": "null"},
        children=[animated_label]
    )
    
    # Start the label faded out
    fx.fade_out(animated_label, duration=0)

    return ui.Column(props={"margin":"20px", "spacing": 10}, children=[
        container,
        ui.Row(props={"spacing": 10}, children=[
            ui.Button("Fade In", on_click=lambda: fx.fade_in(animated_label, 300)),
            ui.Button("Fade Out", on_click=lambda: fx.fade_out(animated_label, 300)),
            ui.Button("Slide In", on_click=slide_in),
        ])
    ])

if __name__ == "__main__":
    winup.run(main_component_path="animation_demo:App", title="Animation Demo")
```

---

# Hot Reloading for Development

WinUp includes a powerful hot-reloading feature to accelerate development. When enabled, any changes you make to your component files will be reflected instantly in your running application without needing a manual restart.

## How it Works

The hot-reloading service monitors your project's Python files. When a change is detected, it intelligently reloads the necessary modules and redraws the UI, preserving the application's state. This is ideal for iterating quickly on UI design and component logic.

## Enabling Hot Reload

To enable hot reloading, you must run your application in development mode. This is done by passing `dev=True` to the `winup.run()` function.

You also need to provide the main component as a string path in the format `"path.to.module:ComponentName"`. This allows WinUp to dynamically re-import your component when the source file changes.

## Example

Here is how you would structure your main application script to use hot reloading:

```python
# main.py
import winup
import sys
import os

# Assume 'my_app' is your components package
from my_app.my_component import App 

if __name__ == "__main__":
    # Add the project root to the path to ensure modules can be found
    project_root = os.path.abspath(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Run the app with hot reloading enabled
    winup.run(
        main_component_path="my_app.my_component:App",
        title="My App with Hot Reload",
        dev=True
    )
```

Now, when you run `python main.py`, any changes you make to `my_app/my_component.py` (or any other component file) will be reflected instantly.