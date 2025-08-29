import winup
from winup import ui

def App():
    return ui.Column(children=[
        ui.Label(text="Image from a local file:"),
        ui.Image(src="", props={}),
    ])

if __name__ == '__main__':
    winup.run(main_component_path="img_err:App")