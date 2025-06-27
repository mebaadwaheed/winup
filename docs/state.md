# State Management in WinUp

WinUp provides a centralized, reactive state management system that makes it easy to manage and synchronize data across your entire application. It's inspired by state management patterns in modern web frameworks like Redux and Vuex but designed with Pythonic simplicity in mind.

The global `winup.state` object is an instance of the `StateManager`, which is the central hub for all state-related operations.

## Core Concepts

### 1. Creating State

The most common way to work with state is by creating a `State` object. This gives you a typed, managed handle to a specific piece of data.

```python
import winup

# Create a state object for a counter
counter_state = winup.state.create("counter", initial_value=0)

# Create a state object for a user's name
username_state = winup.state.create("username", initial_value="Guest")
```

### 2. Getting and Setting State

Once you have a `State` object, you can easily get and set its value.

```python
# Get the current value
current_count = counter_state.get()  # -> 0

# Set a new value
counter_state.set(1)

# The change is reflected immediately
print(counter_state.get())  # -> 1
```
Setting a value will automatically trigger updates in any UI components or functions that are bound or subscribed to that state.

### 3. One-Way Binding (`bind_to`)

This is the most powerful feature of the state manager. You can bind one or more state values to a widget's property. When any of the state values change, the widget's property will be automatically updated.

This is done by calling `.bind_to()` on a `State` object and providing a **formatter function**.

**Example: Binding a Label to the counter**

```python
import winup
from winup import ui

counter_state = winup.state.create("counter", initial_value=0)

@winup.component
def CounterDisplay():
    label = ui.Label()

    # Bind the label's 'text' property to the counter state.
    # The formatter function receives the state's value and returns the new property value.
    counter_state.bind_to(label, "text", formatter=lambda count: f"Current count: {count}")
    
    return label
```

### 4. Multi-State Binding

You can bind a widget to multiple states by chaining them with `.and_()`. The formatter function will receive the values of all the states as arguments, in the order they were chained.

**Example: Combining first and last names**

```python
first_name = winup.state.create("first", "John")
last_name = winup.state.create("last", "Doe")
full_name_label = ui.Label()

# Chain states with .and_() and provide a formatter
first_name.and_(last_name).bind_to(
    full_name_label,
    "text",
    formatter=lambda first, last: f"Full Name: {first} {last}"
)
```

### 5. Subscribing to Changes

If you need to run arbitrary logic when a state changes (not just update a UI property), you can use `.subscribe()`.

```python
def on_count_change(new_count):
    print(f"The count has changed to: {new_count}")

# The callback is called whenever the state is updated
counter_state.subscribe(on_count_change)

# This will trigger the print statement
counter_state.set(5) 
```

### 6. Two-Way Binding (Legacy)

For simple cases like input fields, you can use the legacy `bind_two_way` method. This is less flexible than the new `bind_to` system but can be convenient for simple forms.

```python
# This is a legacy method and may be deprecated in the future.
# Prefer using .bind_to() for one-way data flow and handling input changes separately.
username_input = ui.Input()
winup.state.bind_two_way(username_input, "username")
```
When the user types in the `username_input`, the `"username"` state will be automatically updated. 