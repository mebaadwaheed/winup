# Web State Management

State management in WinUp's web framework is designed to be simple, powerful, and reactive. The core idea is that your application's state lives on the server, and the UI (running in the browser) automatically updates whenever that state changes. This is accomplished using WebSockets.

## Creating State

You create a reactive state variable using `web.state.create()`. This function takes two arguments:
- `key` (str): A unique name for this piece of state.
- `initial_value`: The starting value for the state.

```python
from winup import web

# Create state variables for a counter and a username
counter = web.state.create("counter", 0)
username = web.state.create("username", "Guest")
is_logged_in = web.state.create("is_logged_in", False)
```
These variables can hold any JSON-serializable type (numbers, strings, booleans, lists, dictionaries).

## Binding State to Components

To make your UI reactive, you bind component properties directly to your state variables by name. WinUp provides special `bind_*` props for this.

### One-Way Binding: `bind_text`

Use `bind_text` to make a component's text content update automatically when a state variable changes. This is perfect for labels.

```python
# This label's text will always reflect the current value of the "counter" state.
web.ui.Label(bind_text="counter") 
```

### Two-Way Binding: `bind_value` and `bind_checked`

For input elements, you often need two-way binding: the UI should update when the state changes, and the state should update when the user interacts with the UI.

- `bind_value`: Use this for `<input>` and `<textarea>` elements. When the user types, the new value is sent to the server, updating the state variable, which then broadcasts the change to all other bound elements.
- `bind_checked`: Use this for `<input type="checkbox">` elements. It binds the `checked` property of the checkbox to a boolean state variable.

```python
# This input's value is tied to the "username" state.
web.ui.Input(bind_value="username")

# This checkbox's checked status is tied to the "is_logged_in" state.
web.ui.CheckBox(bind_checked="is_logged_in")
```

## Modifying State in Event Handlers

You modify state from your Python event handlers (e.g., `on_click`). State modification methods are `async`, so your event handlers must be `async def`.

- `state_variable.get()`: Retrieves the current value of the state.
- `state_variable.set(new_value)`: Sets a new value for the state. **This is an `await`-able coroutine.**

```python
# --- State ---
counter = web.state.create("counter", 0)

# --- Event Handler ---
async def increment_counter(event):
    # 1. Get the current value
    current_value = counter.get()
    
    # 2. Set the new value. This is the magic part.
    #    This will automatically update the UI for all connected clients.
    await counter.set(current_value + 1)

# --- Component ---
@web.component
def CounterApp():
    return web.ui.Column(children=[
        web.ui.Label(bind_text="counter"),
        web.ui.Button("Increment", on_click=increment_counter)
    ])
```
When `await counter.set(...)` is called, the server sends a message to the browser over the WebSocket, and the `winup.js` frontend script finds and updates the correct part of the UI. 