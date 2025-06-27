# ProgressBar

The `ProgressBar` widget provides a visual way to indicate the progress of an operation.

## Usage

```python
from winup import ui, winup, state

# Create a state to control the progress bar's value
progress_state = state.create("progress", 0)

@winup.component
def ProgressBarExample():
    
    progress_bar = ui.ProgressBar(min_val=0, max_val=100)

    # Bind the progress bar's value to the state
    progress_state.bind_to(progress_bar, "value", lambda val: val)

    def start_task():
        # In a real app, this would be a background task
        from PySide6.QtCore import QTimer
        def update_progress():
            current_val = progress_state.get()
            if current_val < 100:
                progress_state.set(current_val + 10)
                QTimer.singleShot(500, update_progress)
        update_progress()

    return ui.Column(children=[
        progress_bar,
        ui.Button("Start Progress", on_click=start_task)
    ])
```

## Constructor Parameters

- `min_val: int`: The minimum value of the progress bar. Defaults to `0`.
- `max_val: int`: The maximum value, representing completion. Defaults to `100`.
- `default_val: int`: The initial value of the progress bar. Defaults to `0`.

## Methods

### `.get_value() -> int`
Returns the current value of the progress bar.

### `.set_value(value: int)`
Programmatically sets the current value of the progress bar. 