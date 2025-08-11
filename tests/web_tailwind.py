import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup.web as web

@web.component
def App():
    return web.ui.Column(children=[
        web.ui.Label("Hello", props={'tailwind': 'text-black bg-blue-500 p-4'}),
        web.ui.Label("NO", props={'tailwind': 'text-black bg-blue-500 p-2'})
    ])

if __name__ == '__main__':
    web.web_run(main_component_path="web_tailwind:App", title="FR", reload=True)