import winup
from winup import ui

@winup.component
def RichTextDemo():
    # Create a RichText widget for the demo
    rich_text = ui.RichText(
        text="Welcome to the RichText Demo!\n\n",
        props={
            "min-height": "300px",
            "min-width": "500px",
            "border": "1px solid #ccc",
            "border-radius": "4px",
            "padding": "12px",
            "font-family": "Arial",
            "font-size": "14px",
            "margin-bottom": "10px"
        }
    )

    def add_formatted_sections():
        # Add different formatted sections
        rich_text.append_text(
            "This is bold red text!\n",
            format_dict={
                "color": "red",  # Can use CSS color names
                "bold": True,
                "size": 16
            }
        )
        
        rich_text.append_text(
            "This is italic blue text.\n",
            format_dict={
                "color": "#0000FF",  # Can use hex colors
                "italic": True
            }
        )
        
        rich_text.append_text(
            "This has a yellow background.\n",
            format_dict={
                "background": "yellow"
            }
        )
        
        rich_text.append_text(
            "This is underlined green.\n",
            format_dict={
                "color": "rgb(0, 255, 0)",  # Can use RGB format
                "underline": True
            }
        )

    def add_html_content():
        rich_text.set_html("""
            <h1 style='color: purple;'>HTML Content</h1>
            <p>This content was added using <b>HTML</b>!</p>
            <ul>
                <li>You can use any HTML tags</li>
                <li>With <span style='color: blue;'>custom styling</span></li>
                <li>And <i>formatting</i></li>
            </ul>
        """)

    def clear_content():
        rich_text.clear()

    def show_content():
        # Get and display the content in both plain text and HTML
        plain_text = rich_text.get_text()
        html = rich_text.set_html()
        
        print("Plain Text Content:")
        print(plain_text)
        print("\nHTML Content:")
        print(html)

    # Create a read-only display for comparison
    readonly_rich_text = ui.RichText(
        html="<h3>Read-only RichText</h3><p>This widget is <b>read-only</b> and cannot be edited.</p>",
        read_only=True,
        props={
            "min-height": "100px",
            "background-color": "#f5f5f5",
            "border": "1px solid #ddd",
            "border-radius": "4px",
            "padding": "12px",
            "margin-top": "20px"
        }
    )

    return ui.Column(
        props={"padding": "20px", "margin-bottom": "10px"},
        children=[
            ui.Label(text="RichText Widget Demo", props={"font-size": "24px", "font-weight": "bold", "margin-bottom": "10px"}),
            
            # Main editable RichText
            rich_text,
            
            # Control buttons in a row
            ui.Row(
                props={"margin-bottom": "10px"},
                children=[
                    ui.Button(text="Add Formatted Text", on_click=add_formatted_sections, props={"margin-right": "10px"}),
                    ui.Button(text="Add HTML Content", on_click=add_html_content, props={"margin-right": "10px"}),
                    ui.Button(text="Clear Content", on_click=clear_content, props={"margin-right": "10px"}),
                    ui.Button(text="Show Content", on_click=show_content)
                ]
            ),
            
            # Read-only RichText for comparison
            readonly_rich_text
        ]
    )

if __name__ == "__main__":
    winup.run(main_component_path="rich_text_test:RichTextDemo", title="RichText Widget Demo", dev=True)