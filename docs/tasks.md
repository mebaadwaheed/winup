# Asynchronous Task Runner

Modern desktop applications often need to perform long-running operations, such as making network requests, accessing a database, or processing a large file. If you run these operations on the main UI thread, your application will freeze and become unresponsive.

WinUp provides a simple and elegant solution to this problem with its built-in, asynchronous task runner. It allows you to run any function on a background thread with a simple decorator, ensuring your UI remains smooth and responsive.

The global `winup.tasks` module provides the `run` decorator.

## How to Use It

The `@tasks.run()` decorator can be applied to any function you want to run in the background. It takes optional callback functions (`on_finish`, `on_error`, `on_start`) as arguments.

```python
from winup import tasks, ui
import time

# A state to hold the result from our background task
status_state = winup.state.create("status", "Idle")

@tasks.run(
    on_start=lambda: status_state.set("Loading..."),
    on_finish=lambda result: status_state.set(f"Success: {result}"),
    on_error=lambda error: status_state.set(f"Error: {error[0]}")
)
def fetch_data_from_server(url: str):
    """A simulated long-running task."""
    print(f"Fetching data from {url} on a background thread...")
    time.sleep(3) # Simulate network latency
    if url == "bad_url":
        raise ConnectionError("Could not connect to server.")
    return "Data fetched successfully!"

# --- In your UI ---

@winup.component
def MyComponent():
    status_label = ui.Label()
    status_state.bind_to(status_label, "text", formatter=lambda status: f"Status: {status}")

    return ui.Column(children=[
        status_label,
        ui.Button(
            text="Fetch Good Data",
            on_click=lambda: fetch_data_from_server("good_url")
        ),
        ui.Button(
            text="Fetch Bad Data (to test error)",
            on_click=lambda: fetch_data_from_server("bad_url")
        )
    ])
```

## Decorator Arguments

- `on_start: callable` (optional): A function that will be called on the main UI thread just before the background task begins. It takes no arguments.
- `on_finish: callable` (optional): A function that will be called on the main UI thread if the background task completes successfully. It receives the return value of your function as its only argument.
- `on_error: callable` (optional): A function that will be called on the main UI thread if the background task raises an exception. It receives a tuple containing the exception object and its traceback string as its only argument.

## How It Works

WinUp's `TaskManager` maintains a `QThreadPool` of background worker threads. When you call a function decorated with `@tasks.run`, the following happens:
1.  The `on_start` callback is immediately executed on the main thread.
2.  A `Worker` (a `QRunnable`) is created, which wraps your function and its arguments.
3.  The `Worker` is submitted to the `QThreadPool` and begins executing your function on a background thread.
4.  When your function finishes, the `Worker` emits a Qt signal (`finished` or `error`) on the background thread.
5.  Because of Qt's cross-thread signal/slot mechanism, the connected callback (`on_finish` or `on_error`) is safely executed back on the main UI thread, where it is safe to update widgets and application state. 