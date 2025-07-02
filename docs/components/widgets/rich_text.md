# RichText

The `RichText` widget is a rich text editor that supports formatted text, HTML content, and dynamic text styling.

## Usage

```python
from winup import ui, winup

@winup.component
def RichTextExample():
    def add_formatted_text():
        rich_text.append_text(
            "This is red and bold text!\n",
            format_dict={
                "color": "red",
                "bold": True,
                "size": 14
            }
        )

    rich_text = ui.RichText(
        text="Initial plain text",
        props={
            "min-height": "200px",
            "border": "1px solid #ccc",
            "border-radius": "4px",
            "padding": "8px"
        }
    )

    return ui.Column(children=[
        # A simple rich text editor
        rich_text,

        # A read-only rich text display with HTML content
        ui.RichText(
            html="<h1>Hello World</h1><p>This is <b>formatted</b> text with <span style='color: blue;'>colors</span>!</p>",
            read_only=True
        ),

        # A button to add formatted text
        ui.Button(text="Add Formatted Text", on_click=add_formatted_text)
    ])
```

## Constructor Parameters

- `text: str`: The initial plain text content. Defaults to `""`.
- `html: str`: The initial HTML content. If provided, takes precedence over `text`. Defaults to `""`.
- `props: dict` (optional): A dictionary of style properties to apply to the widget.
- `read_only: bool`: If `True`, the content cannot be edited by the user. Defaults to `False`.

## Methods

### `.set_text(text: str)`

A Pythonic alias for `setPlainText()`. Sets the widget's content as plain text.

```python
rich_text = ui.RichText()
rich_text.set_text("Hello World!")
```

### `.set_html(html: str)`

A Pythonic alias for `setHtml()`. Sets the widget's content as HTML.

```python
rich_text = ui.RichText()
rich_text.set_html("<h1>Hello</h1><p>This is <b>HTML</b> content!</p>")
```

### `.append_text(text: str, format_dict: dict = None)`

Appends text to the end of the current content with optional formatting.

- `text`: The text to append
- `format_dict`: Optional dictionary of text formatting properties:
  - `"color"`: Text color (e.g., `"red"`, `"#FF0000"`)
  - `"background"`: Background color
  - `"bold"`: Boolean for bold text
  - `"italic"`: Boolean for italic text
  - `"underline"`: Boolean for underlined text
  - `"size"`: Font size in points

```python
rich_text = ui.RichText()
rich_text.append_text(
    "Important warning!",
    format_dict={
        "color": "red",
        "bold": True,
        "size": 14
    }
)
```

### `.clear()`

A Pythonic alias for `clear()`. Removes all content from the widget.

### `.get_text() -> str`

A Pythonic alias for `toPlainText()`. Returns the current content as plain text.

### `.get_html() -> str`

A Pythonic alias for `toHtml()`. Returns the current content as HTML. 