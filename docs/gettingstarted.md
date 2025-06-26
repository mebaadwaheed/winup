# Installation

```bash
pip install winup
```
*The `watchdog` library is required for the Hot Reloading feature.*

```bash
winup init
```

*This makes an app template ready for use, if LoadUp doesn't work, use PyInstaller instead.*


# Getting Started: Hello, WinUp!

Creating an application is as simple as defining a main component and running it.

```python
# hello_world.py
import winup
from winup import ui

# The @component decorator is optional for the main component, but good practice.
@winup.component
def App():
    """This is our main application component."""
    return ui.Column(
        props={
            "alignment": "AlignCenter", 
            "spacing": 20
        },
        children=[
            ui.Label("👋 Hello, WinUp!", props={"font-size": "24px"}),
            ui.Button("Click Me!", on_click=lambda: print("Button clicked!"))
        ]
    )

if __name__ == "__main__":
    winup.run(main_component_path="hello_world:App", title="My First WinUp App")
```