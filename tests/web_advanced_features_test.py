# tests/web_advanced_features_test.py
import sys
import os
import time
import asyncio

# Add project root for local testing
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from winup import web
except ImportError:
    print("Please install web dependencies first: pip install .[web]")
    sys.exit(1)

# --- 1. State Management ---
task_status = web.state.create("task_status", "Idle")
task_result = web.state.create("task_result", "N/A")
memo_render_count = 0  # Use a global to track actual renders

# --- 2. Profiler & Memoization Demo ---
@web.memo.memo
@web.profiler.get_profiler().measure("MemoizedCard")
@web.component
def MemoizedCard(title: str):
    """A component that is expensive to render to test memoization."""
    global memo_render_count
    memo_render_count += 1
    # Simulate a complex render
    time.sleep(0.1) 
    return web.ui.Column(
        style={'padding': '0.5rem', 'border': '1px solid green', 'margin_top': '0.5rem'},
        children=[
            web.ui.Label(f"Title: {title}"),
            web.ui.Label(f"(This component has been fully rendered {memo_render_count} time(s))")
        ]
    )

# --- 3. Task Runner Demo ---
# --- Callbacks ---
async def on_task_start():
    await task_status.set("Running...")
    await task_result.set("...")

async def on_task_finish(result):
    await task_status.set("Success!")
    await task_result.set(str(result))

async def on_task_error(error):
    await task_status.set("Error!")
    await task_result.set(str(error))

# --- Tasks ---
@web.tasks.run(on_start=on_task_start, on_finish=on_task_finish, on_error=on_task_error)
@web.profiler.get_profiler().measure("successful_sync_task")
def successful_sync_task(event):
    """A sync task that runs in a background thread."""
    print("Running sync task...")
    time.sleep(2)
    print("Sync task finished.")
    return "Sync task completed successfully."

@web.tasks.run(on_start=on_task_start, on_finish=on_task_finish, on_error=on_task_error)
async def successful_async_task(event):
    """An async task that runs on the main event loop."""
    print("Running async task...")
    await asyncio.sleep(2)
    print("Async task finished.")
    return "Async task completed successfully."

@web.tasks.run(on_start=on_task_start, on_finish=on_task_finish, on_error=on_task_error)
def error_task(event):
    """A task designed to fail."""
    print("Running a task that will fail...")
    time.sleep(1)
    raise ValueError("This task was designed to fail.")

# --- 4. Main Application Component ---
def Card(title: str, children: list):
    """A simple, reusable card component for styling."""
    return web.ui.Column(
        style={'padding': '1rem', 'border': '1px solid #ddd', 'border_radius': '8px', 'background_color': '#f9f9f9', 'margin_top': '1rem'},
        children=[web.ui.Label(title, style={'font_weight': 'bold', 'font_size': '1.2rem'}), *children]
    )

@web.component
def App():
    """The main application component."""
    return web.ui.Column(
        style={'padding': '2rem', 'max_width': '800px', 'margin': 'auto'},
        children=[
            web.ui.Label("Advanced Features Test", style={'font_size': '2em'}),

            # Task Runner Test
            Card("Task Runner", children=[
                web.ui.Label("Status:", style={'font_weight': 'bold'}),
                web.ui.Label(bind_text="task_status"),
                web.ui.Label("Result:", style={'font_weight': 'bold', 'margin_top': '0.5rem'}),
                web.ui.Label(bind_text="task_result", style={'font_family': 'monospace'}),
                web.ui.Row(gap="10px", style={'margin_top': '1rem'}, children=[
                    web.ui.Button("Run Sync Task (2s)", on_click=successful_sync_task),
                    web.ui.Button("Run Async Task (2s)", on_click=successful_async_task),
                    web.ui.Button("Run Failing Task", on_click=error_task),
                ])
            ]),

            # Memoization & Profiler Test
            Card("Memoization & Profiler", children=[
                web.ui.Label("The MemoizedCard component is rendered multiple times below."),
                web.ui.Label("Thanks to @web.memo, its body only executes when props change."),
                MemoizedCard("Card A"),
                MemoizedCard("Card A"), # Cache hit
                MemoizedCard("Card B"), # Cache miss
                MemoizedCard("Card A"), # Cache hit
            ]),
            
            # Profiler Link
            Card("Profiler Results", children=[
                web.ui.Label("The profiler is measuring the render time of MemoizedCard and the execution time of the sync task."),
                web.ui.Link(
                    "View Profiler Results", 
                    href="/_winup/profiler", 
                    props={'target': '_blank'},
                    style={'margin_top': '1rem', 'display': 'inline-block'}
                )
            ]),
        ]
    )

# --- 5. Run the App ---
if __name__ == "__main__":
    web.web_run(
        main_component_path="web_advanced_features_test:App", 
        title="Advanced Web Features Test",
        reload=True
    ) 