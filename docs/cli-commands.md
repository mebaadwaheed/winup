# WinUp CLI Commands Documentation

## Overview

The WinUp CLI provides commands for running applications, initializing projects, and managing cross-platform development workflows.

## Installation & Access

```bash
pip install winup
winup --help
```

## Commands

### `winup run`

Run a WinUp application with platform selection and configuration options.

#### Basic Syntax
```bash
winup run <app_path> [OPTIONS]
```

#### Platform Selection
```bash
# Desktop mode (default)
winup run examples.layout_showcase:LayoutApp --desktop

# Web mode
winup run examples.layout_showcase:LayoutApp --web

# Auto-detect platform (defaults to desktop)
winup run examples.layout_showcase:LayoutApp
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--desktop` | flag | False | Run in desktop mode |
| `--web` | flag | False | Run in web mode |
| `--title` | string | 'WinUp App' | Application window title |
| `--width` | integer | 800 | Application window width (desktop only) |
| `--height` | integer | 600 | Application window height (desktop only) |
| `--web-port` | integer | 8000 | Port for web server (web mode only) |
| `--web-title` | string | None | Title for web page (overrides --title in web mode) |
| `--web-favicon` | string | None | Path to favicon for web page |
| `--web-metadata` | string | None | Additional metadata for web page (JSON string) |
| `--web-router` | string | None | Router path for web routing (format: module.path:router) |
| `--web-reload` | flag | False | Enable hot reload for web mode |
| `--reload` | flag | False | Enable hot reload for development |
| `--router` | string | None | Router path for web routing (alias for --web-router) |
| `--shell` | string | None | App shell path for web routing (format: module.path:component) |

#### Examples

**Desktop Application**
```bash
winup run tests.cli_test_app:App --desktop --title "My Desktop App" --width 1024 --height 768
```

**Web Application**
```bash
winup run tests.cli_test_app:App --web --web-port 8080 --web-title "My Web App"
```

**Web Application with Routing**
```bash
winup run tests.unified_routing_test:HomePage --web \
  --router tests.unified_routing_test:app_router \
  --shell tests.unified_routing_test:AppShell \
  --web-port 8003
```

**Development Mode with Hot Reload**
```bash
winup run examples.counter_app:App --desktop --reload
winup run examples.counter_app:App --web --web-reload
```

**Web Application with Metadata**
```bash
winup run app:MainApp --web \
  --web-title "My Amazing App" \
  --web-favicon "assets/favicon.ico" \
  --web-metadata '{"description": "A cross-platform app", "keywords": "winup,python,gui"}'
```

### `winup init`

Initialize a new WinUp project with scaffolding and configuration.

#### Syntax
```bash
winup init
```

#### Interactive Setup
The command will prompt for:
- **Project name**: Name of your new project
- **Icepack integration**: Plugin management system (experimental)
- **LoadUp integration**: Executable building system

#### Generated Structure
```
my-winup-app/
├── .gitignore
├── README.md
├── winup.config.json
├── src/
│   └── app/
│       ├── main.py
│       └── components/
│           └── card.py
├── assets/
└── web/
    └── src/
        └── app/
            └── components/
```

#### Generated Files

**`src/app/main.py`** - Main application entry point
```python
import winup
from winup import ui
from components.card import Card

@winup.component
def App():
    return ui.Column(
        props={"alignment": "AlignCenter", "spacing": 20},
        children=[
            Card("Welcome to WinUp!"),
            ui.Label("Edit `src/app/main.py` to get started."),
        ]
    )

if __name__ == "__main__":
    winup.run(main_component_path="app.main:App", title="my-winup-app", dev=True)
```

**`winup.config.json`** - Project configuration
```json
{
    "project_name": "my-winup-app",
    "version": "0.1.0",
    "main_file": "src/app/main.py"
}
```

## App Path Format

The `app_path` parameter uses Python module notation:

```bash
# Format: module.path:ComponentName
winup run examples.counter_app:App
winup run src.app.main:MainApp
winup run components.dashboard:Dashboard
```

## Platform Auto-Detection

When no platform flags are specified:
- Defaults to **desktop** mode
- Can be overridden by setting environment variables
- Platform is set automatically before component execution

## Error Handling

### Invalid Platform Combination
```bash
winup run app:App --web --desktop
# Error: Cannot specify both --web and --desktop flags
```

### Missing Component
```bash
winup run nonexistent.module:App
# Error: Module 'nonexistent.module' not found
```

### Platform Compatibility
```bash
winup run desktop_only_app:App --web
# Error: Component 'App' is not supported on platform 'web'
```

## Development Workflow

### 1. Create New Project
```bash
winup init
cd my-winup-app
```

### 2. Develop Desktop Version
```bash
winup run src.app.main:App --desktop --reload
```

### 3. Test Web Version
```bash
winup run src.app.main:App --web --web-reload --web-port 8080
```

### 4. Deploy Cross-Platform
```bash
# Desktop distribution
python -m PyInstaller src/app/main.py

# Web deployment
winup run src.app.main:App --web --web-port 80
```

## Configuration Files

### `winup.config.json`
Project-level configuration for WinUp applications.

```json
{
    "project_name": "my-app",
    "version": "1.0.0",
    "main_file": "src/app/main.py",
    "web": {
        "port": 8000,
        "title": "My Web App",
        "favicon": "assets/favicon.ico"
    },
    "desktop": {
        "width": 1024,
        "height": 768,
        "title": "My Desktop App"
    }
}
```

### `ice.config.json` (Optional)
Plugin management configuration for Icepack integration.

```json
{
    "plugins": [
        "winup-charts",
        "winup-database"
    ]
}
```

### `loadup.config.json` (Optional)
Executable building configuration for LoadUp integration.

```json
{
    "build_dir": "dist",
    "icon": "assets/icon.ico",
    "name": "MyApp"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WINUP_PLATFORM` | Force platform selection | None |
| `WINUP_DEV_MODE` | Enable development features | False |
| `WINUP_WEB_PORT` | Default web server port | 8000 |

## Integration Examples

### With Hot Reload
```bash
# Desktop development
winup run app:App --desktop --reload --title "Dev Mode"

# Web development  
winup run app:App --web --web-reload --web-port 3000
```

### With Routing
```bash
winup run pages.home:HomePage --web \
  --router router:app_router \
  --shell components.shell:AppShell
```

### Production Deployment
```bash
# Production web server
winup run app:App --web --web-port 80 --web-title "Production App"

# Desktop executable
winup run app:App --desktop --title "Production App"
```
