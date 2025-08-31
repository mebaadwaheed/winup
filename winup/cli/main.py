import click
import questionary
import os
import json
import subprocess
from pathlib import Path

# --- File Templates ---

GITIGNORE_CONTENT = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.idea/
.vscode/
"""

README_CONTENT = """
# {project_name}

A new desktop application built with WinUp.

## Getting Started

First, make sure you have WinUp installed.
```bash
pip install winup
```

## Running the Application

To run your new application, execute the main script from the project root:
```bash
python src/app/main.py
```

This will launch your application window. You can start editing the files in `src/app` to build your UI.
"""

APP_MAIN_PY_CONTENT = """
import sys
import os

# This ensures the app can find its own modules.
# It adds the 'src' directory to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import winup
from winup import ui
from components.card import Card

@winup.component
def App():
    \"\"\"The main application component.\"\"\"
    return ui.Column(
        props={{"alignment": "AlignCenter", "spacing": 20}},
        children=[
            Card("Welcome to WinUp!"),
            ui.Label("Edit `src/app/main.py` to get started."),
        ]
    )

if __name__ == "__main__":
    winup.run(main_component_path="app.main:App", title="{project_name}", dev=True)
"""

BASE_COMPONENT_CONTENT = """
from winup import ui

def Card(text: str):
    \"\"\"A simple card component.\"\"\"
    return ui.Frame(
        props={
            "class": "card",
            "padding": "20px",
            "background-color": "#f0f0f0",
            "border-radius": "10px"
        },
        children=[
            ui.Label(text, props={"font-size": 24})
        ]
    )
"""



WINUP_CONFIG_CONTENT = {
    "project_name": "{project_name}",
    "version": "0.1.0",
    "main_file": "src/app/main.py"
}

@click.group()
def cli():
    """WinUp Framework CLI"""
    pass

@cli.command()
@click.argument('app_path')
@click.option('--desktop', is_flag=True, default=False, help='Run in desktop mode')
@click.option('--web', is_flag=True, default=False, help='Run in web mode')
@click.option('--title', default='WinUp App', help='Application window title')
@click.option('--width', default=800, help='Application window width')
@click.option('--height', default=600, help='Application window height')
@click.option('--web-port', default=8000, help='Port for web server (web mode only)')
@click.option('--web-title', help='Title for web page (overrides --title in web mode)')
@click.option('--web-favicon', help='Path to favicon for web page')
@click.option('--web-metadata', help='Additional metadata for web page (JSON string)')
@click.option('--web-router', help='Router path for web routing (format: module.path:router)')
@click.option('--web-reload', is_flag=True, default=False, help='Enable hot reload for web mode')
@click.option('--reload', is_flag=True, default=False, help='Enable hot reload for development')
@click.option('--router', help='Router path for web routing (format: module.path:router)')
@click.option('--shell', help='App shell path for web routing (format: module.path:component)')
def run(app_path, desktop, web, title, width, height, web_port, web_title, web_favicon, web_metadata, web_router, web_reload, reload, router, shell):
    """Run a WinUp application with platform selection."""
    import sys
    import winup
    from winup.core.platform import set_platform
    
    # Add current directory to Python path for module resolution
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    
    # Determine platform
    if web and desktop:
        click.secho("Error: Cannot specify both --web and --desktop flags", fg="red")
        return
    elif web:
        platform = 'web'
    elif desktop:
        platform = 'desktop'
    else:
        # Default to desktop if no platform specified
        platform = 'desktop'
    
    # Set the platform before running
    set_platform(platform)
    
    click.echo(f"Running {app_path} in {platform} mode...")
    
    try:
        if platform == 'web':
            # Parse web metadata if provided
            parsed_metadata = None
            if web_metadata:
                try:
                    import json
                    parsed_metadata = json.loads(web_metadata)
                except json.JSONDecodeError:
                    click.secho("Warning: Invalid JSON in --web-metadata, ignoring", fg="yellow")
            
            # Use new winup.run() with web parameters
            winup.run(
                app_path, 
                platform='web',
                title=title,
                web_title=web_title,
                web_port=web_port,
                web_favicon=web_favicon,
                web_metadata=parsed_metadata,
                web_router=web_router or router,
                web_reload=web_reload,
                dev=reload
            )
        else:
            # Use desktop runner
            winup.run(app_path, title=title, width=width, height=height, dev=reload)
    except Exception as e:
        click.secho(f"Error running application: {e}", fg="red")

@cli.command()
def init():
    """Initializes a new WinUp project."""
    click.echo("🚀 Welcome to WinUp! Let's create a new project.")

    project_name = questionary.text(
        "What is the name of your project?",
        default="my-winup-app"
    ).ask()

    use_icepack = questionary.confirm(
        "Use Icepack 0.1.0 for plugin management (Wont work fully yet...)?",
        default=False
    ).ask()

    use_loadup = questionary.confirm(
        "Use LoadUp 0.1.0 for building executables?",
        default=False
    ).ask()

    # --- Project Scaffolding ---
    try:
        project_path = Path(project_name)
        if project_path.exists():
            click.secho(f"Error: Directory '{project_name}' already exists.", fg="red")
            return

        # Create directories
        src_path = project_path / "src" / "app" / "components"
        web_path = project_path / "web" / "src" / "app" / "components"
        assets_path = project_path / "assets"
        src_path.mkdir(parents=True, exist_ok=True)
        assets_path.mkdir(exist_ok=True)

        # Create files
        (project_path / ".gitignore").write_text(GITIGNORE_CONTENT)
        (project_path / "README.md").write_text(README_CONTENT.format(project_name=project_name))
        (src_path.parent / "main.py").write_text(APP_MAIN_PY_CONTENT.format(project_name=project_name))
        (src_path / "card.py").write_text(BASE_COMPONENT_CONTENT)
        
        # Create config files
        config = WINUP_CONFIG_CONTENT.copy()
        config["project_name"] = project_name
        (project_path / "winup.config.json").write_text(json.dumps(config, indent=4))

        if use_icepack:
            (project_path / "ice.config.json").write_text(json.dumps({"plugins": []}, indent=4))
        
        if use_loadup:
            subprocess.run(["pip", "install", "loadup"], cwd=project_path)
            (project_path / "loadup.config.json").write_text(json.dumps({"build_dir": "dist"}, indent=4))

        # Initialize Git repo
        subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)

        click.secho(f"\n✅ Success! Your new WinUp project '{project_name}' is ready.", fg="green")
        click.echo("\nTo get started:")
        click.echo(f"  cd {project_name}")
        click.echo(f"  python src/app/main.py")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")

if __name__ == "__main__":
    cli() 