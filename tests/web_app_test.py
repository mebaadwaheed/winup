import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from winup import web
except ImportError:
    print("Could not import winup.web. Make sure you are running from the project root.")
    sys.exit(1)

# A simple state holder
app_state = {}

@web.component
def App():
    """The main application component."""

    def on_mount():
        print("App component mounted!")
        if 'animated_label' in app_state:
            app_state['animated_label'].set_visibility(False)

    def toggle_theme():
        current = web.web_theme_manager.get_active_theme_name()
        next_theme = "dark" if current == "light" else "light"
        web.web_theme_manager.set_theme(next_theme)
        web.ui.notify(f"Switched to {next_theme} theme")

    def toggle_animation():
        label = app_state.get('animated_label')
        if label:
            if not label.visible:
                label.set_visibility(True)
                # Add a tiny delay to allow the browser to render the element
                # before applying the animation class.
                web.ui.timer(0.01, lambda: web.animate.fade_in(label), once=True)
            else:
                web.animate.fade_out(label)
                web.ui.timer(0.5, lambda: label.set_visibility(False), once=True)

    # We need to render the label and store a reference to it.
    animated_label = web.ui.Label("I'm animated!")
    app_state['animated_label'] = animated_label

    return web.ui.Column([
        web.ui.Label("Hello from WinUp on the Web!").style("font-size: 2em; font-weight: bold; padding: 1rem;"),
        web.ui.Button("Toggle Theme", on_click=toggle_theme).style("background-color: var(--primary-color); color: var(--primary-text-color)"),
        web.ui.Button("Toggle Animation", on_click=toggle_animation),
        animated_label,
    ])

if __name__ in {"__main__", "__mp_main__"}:
    web.web_run("tests.web_app_test:App", title="WinUp Web Test", reload=True) 