# Live Hot Reload (LHR)

Live Hot Reload is one of WinUp's standout features, designed to dramatically speed up your development workflow. It allows you to see your UI changes instantly without needing to restart your entire application every time you save a file.

## How it Works

The hot reload service uses the `watchdog` library to monitor your project's Python files for changes. When a change is detected, WinUp intelligently reloads the relevant module in memory and triggers a redraw of your main component. This means the application state is preserved, and the UI is updated on the fly.

- **Cross-thread Communication:** The file system watcher runs in a background thread to avoid blocking the UI. It uses Qt's signal and slot mechanism to safely notify the main GUI thread that a reload is needed.
- **Intelligent Reloading:** WinUp reloads only the modules that have changed, which is fast and efficient. It can even handle changes in the `__main__` script.
- **Error Handling:** If you introduce a syntax error or a runtime error into your code, the hot reloader will print the traceback to the console without crashing the application. Once you fix the error and save the file, the UI will reload as expected.

## How to Use It

Live Hot Reload is enabled by default when you create a new project with `winup init`. The magic happens in a single argument passed to the `winup.run()` function.

```python
# In your main.py

if __name__ == "__main__":
    winup.run(
        main_component_path="app.main:App", # Path to your main component
        title="My Hot-Reloaded App",
        dev=True  # This is the key!
    )
```

### `main_component_path`

Instead of passing the component function directly, you pass a string path to it in the format `"module.path:AttributeName"`. This allows WinUp to re-import the component dynamically from its source file every time a change is detected.

### `dev=True`

Setting the `dev` flag to `True` is what activates the hot reload service. When you are ready to build your application for production, you should typically remove this flag or set it to `False`.

## What Gets Reloaded?

- **UI and Logic:** Any changes to your component files, including layouts, styles, and event handlers, will be reflected immediately.
- **Helper Functions:** Changes in any other Python files within your project directory will also trigger a reload.

## What Does NOT Get Reloaded?

- **Application State:** The state managed by `winup.state` is preserved across reloads. This is a powerful feature, as it allows you to tweak the UI without losing your application's current data.
- **External Libraries:** Files in `site-packages` (your installed dependencies) are not watched for changes.
- **Non-Python Files:** Changes to assets like images or data files will not trigger a reload. 