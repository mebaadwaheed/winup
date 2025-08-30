import winup
from winup import ui

def App():
    return ui.TreeView(
        data={"group1": ["item1", "item2", "item3"], "group2": ["item4", "item5", "item6"]},
        on_select=lambda x: print(x),
        props={"background-color": "white"}  # Now supported
    )

if __name__ == "__main__":
    winup.run(main_component_path="tree:App")