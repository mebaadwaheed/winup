# Input

The `Input` widget is a standard single-line text entry field. It's used to get text input from the user. It includes built-in support for placeholders, validation, and submission events.

## Usage

```python
from winup import ui, winup

@winup.component
def InputExample():
    def on_submit():
        print("Enter key was pressed!")

    def on_change(text):
        print(f"Text changed to: {text}")

    return ui.Column(children=[
        # A simple input with a placeholder
        ui.Input(placeholder="Enter your name..."),

        # An input with event handlers
        ui.Input(
            placeholder="Type and press Enter",
            on_submit=on_submit,
            on_text_changed=on_change
        ),

        # An input with built-in email validation
        ui.Input(
            placeholder="Enter your email",
            validation="email"
        )
    ])
```

By default, when using validation, the input field will get a `"valid"` or `"invalid"` class applied to it. You can use these classes in your global stylesheet to provide visual feedback.

```python
# In your global styles
style.add_style_dict({
    "Input.valid": {
        "border": "2px solid green"
    },
    "Input.invalid": {
        "border": "2px solid red"
    }
})
```

## Constructor Parameters

- `placeholder: str`: The placeholder text to display when the input is empty.
- `text: str`: The initial text value of the input.
- `props: dict` (optional): A dictionary of style properties.
- `validation`: (optional) The validation rule to apply. Can be:
    - A string for a built-in rule: `"email"`, `"integer"`, `"decimal"`.
    - A compiled regex pattern (`re.Pattern`).
    - A custom function that takes the text as a string and returns `True` if valid, `False` otherwise.
- `on_submit: callable` (optional): A function to call when the user presses the Enter or Return key.
- `on_text_changed: callable` (optional): A function to call whenever the text in the input changes. It receives the new text as its only argument.

## Methods

### `.set_text(text: str)`
Sets the text of the input field programmatically.

### `.get_text() -> str`
Returns the current text from the input field.

### `.clear()`
Clears all text from the input field. 