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