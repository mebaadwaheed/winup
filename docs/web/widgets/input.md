# Input

The `Input` component renders a standard HTML `<input>` element and is the primary way to collect text-based user input. It is designed for two-way data binding.

## Usage

The most common use case is to bind the input's value to a state variable.

```python
from winup import web

# Create a state variable to hold the input's value
username = web.state.create("username", "")

@web.component
def LoginForm():
    return web.ui.Column(children=[
        web.ui.Label("Enter your name:"),
        
        # This input has two-way binding to the "username" state.
        # Typing in the box updates the server state, which updates
        # all other bound elements.
        web.ui.Input(
            bind_value="username",
            placeholder="e.g., Jane Doe"
        ),
        
        # A label to show the reactive changes
        web.ui.Label(bind_text="username")
    ])
```

## Arguments
- `bind_value` (str, optional): The key of a state variable to bind the input's value to. This enables two-way data binding.
- `placeholder` (str, optional): The placeholder text to display when the input is empty.
- `props` (dict, optional): A dictionary of additional HTML attributes. You can set the input `type` here (e.g., `props={'type': 'password'}`).
- `**kwargs`: Keyword arguments are also treated as HTML attributes.

## Two-Way Data Binding

When you use `bind_value`:
1.  **Server to Client**: If the state variable is changed on the server (e.g., `await username.set("Default")`), the new value is sent to the browser and the input field's value is updated.
2.  **Client to Server**: When the user types into the input field, a message is sent to the server over the WebSocket, updating the state variable. This change is then broadcast to all other elements bound to that same state key. 