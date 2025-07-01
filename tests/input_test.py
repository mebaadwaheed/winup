import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import winup
from winup.ui.widgets.input import Input as DefaultInput


class PasswordInput(DefaultInput):
    """An Input that hides text by default but has a toggle button."""
    def __init__(self, props: dict = {}):
        super().__init__(props=props)
        # In a real implementation, you would add a button here
        # and connect it to self.setEchoMode().
        self.setEchoMode(self.EchoMode.Password)


winup.ui.register_widget("PasswordInput", PasswordInput)

@winup.component
def App():
    return winup.ui.Column(
        children=[
            winup.ui.Label("Password Input"),
            PasswordInput()
        ]
    )

if __name__ == "__main__":
    winup.run(main_component_path="tests.e:App", title="Password Input")