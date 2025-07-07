# Web Task Runner

Modern web applications often need to perform long-running operations without blocking the server or freezing the user interface. Examples include making API calls to external services, querying a database, or performing CPU-intensive computations.

WinUp's web framework provides a simple and powerful asynchronous task runner that integrates seamlessly with its reactive state management system.

## How to Use It

The `@web.tasks.run()` decorator can be applied to any function you want to run in the background. It takes optional callback functions (`on_start`, `on_finish`, `on_error`) as arguments.

Because the task runner is integrated with the web server's `asyncio` event loop, your callback functions **must be `async`** if they modify application state.

```python
from winup import web
import asyncio
import time

# A state to hold the result from our background task
status = web.state.create("status", "Idle")

# --- Callbacks (must be async to modify state) ---
async def handle_start():
    await status.set("Fetching data from server...")

async def handle_finish(result):
    await status.set(f"Success: {result}")

async def handle_error(error):
    await status.set(f"Error: {error}")

# --- Background Task ---
@web.tasks.run(
    on_start=handle_start,
    on_finish=handle_finish,
    on_error=handle_error
)
def fetch_data(fail: bool = False):
    """
    A simulated long-running task. This function itself can be
    synchronous (blocking); the decorator will run it in a separate
    thread to avoid blocking the server's event loop.
    """
    print("Task started on a background thread...")
    time.sleep(2)
    if fail:
        raise ConnectionError("Could not connect.")
    return "Data fetched!"

# --- UI Component ---
@web.component
def TaskRunnerDemo():
    return web.ui.Column(children=[
        web.ui.Label(bind_text="status"),
        web.ui.Button("Run Success Task", on_click=lambda e: fetch_data(fail=False)),
        web.ui.Button("Run Failing Task", on_click=lambda e: fetch_data(fail=True)),
    ])
```

## Decorator Arguments

- `on_start: callable` (optional): An `async` or `sync` function called just before the task begins.
- `on_finish: callable` (optional): An `async` or `sync` function called if the task completes successfully. It receives the task's return value as its only argument.
- `on_error: callable` (optional): An `async` or `sync` function called if the task raises an exception. It receives the exception object as its only argument.

## How It Works

1.  **Event Trigger**: A user action (like a button click) calls your decorated function (`fetch_data`).
2.  **Task Scheduling**: The `@web.tasks.run` decorator creates a background task using `asyncio.create_task`.
3.  **Callbacks**: The `on_start` callback is immediately called.
4.  **Execution**:
    - If your decorated function is `async`, it is `await`ed directly within the background task.
    - If your decorated function is synchronous (blocking), the task runner automatically runs it in a separate thread using `run_in_executor` to prevent it from blocking the main server event loop.
5.  **Result Handling**: When the function completes, the `on_finish` (on success) or `on_error` (on failure) callback is called with the result or exception.
6.  **UI Update**: If your callbacks modify the application state (e.g., `await status.set(...)`), the changes are automatically broadcast to the browser via WebSocket, updating the UI. 