# Graphing Widgets

WinUp includes a powerful and easy-to-use set of graphing widgets built on `QtCharts`. These widgets are designed to be stylish, animated, and seamlessly integrate with your application's theme. They all support dynamic data updates via a simple `set_data()` method.

## Bar Chart
Use a `BarChart` to compare values across different categories.

```python
import winup
from winup import ui
import random

def App():
    bar_data = {"Apples": 12, "Oranges": 25, "Bananas": 8}
    chart = ui.BarChart(data=bar_data, title="Fruit Distribution")
    
    def randomize_data():
        new_data = {k: random.randint(5, 30) for k in bar_data}
        chart.set_data(new_data)

    return ui.Column([chart, ui.Button("Randomize", on_click=randomize_data)])

# To run this, you would need a WinUp app instance.
# Example: winup.run(main_component_path="graph_demo:App", title="Bar Chart Demo")
```

## Line Chart
A `LineChart` is perfect for showing trends over time or continuous data.

```python
import winup
from winup import ui
import random

def App():
    line_data = {"Sales": [(2020, 100), (2021, 150), (2022, 130), (2023, 180)]}
    chart = ui.LineChart(data=line_data, title="Annual Sales")
    
    def randomize_data():
        new_data = {"Sales": [(y, random.randint(80, 200)) for y, _ in line_data["Sales"]]}
        chart.set_data(new_data)

    return ui.Column([chart, ui.Button("Randomize", on_click=randomize_data)])

# To run this, you would need a WinUp app instance.
# Example: winup.run(main_component_path="graph_demo:App", title="Line Chart Demo")
```

## Pie Chart
Use a `PieChart` (rendered as a modern donut chart) to show the proportions of a whole.

```python
import winup
from winup import ui
import random

def App():
    pie_data = {"Desktop": 60, "Mobile": 30, "Tablet": 10}
    chart = ui.PieChart(data=pie_data, title="Device Usage")
    
    def randomize_data():
        new_data = {k: random.randint(10, 80) for k in pie_data}
        chart.set_data(new_data)

    return ui.Column([chart, ui.Button("Randomize", on_click=randomize_data)])

# To run this, you would need a WinUp app instance.
# Example: winup.run(main_component_path="graph_demo:App", title="Pie Chart Demo")
```

## Scatter Plot
A `ScatterPlot` is ideal for visualizing the relationship between two numerical variables.

```python
import winup
from winup import ui
import random

def App():
    scatter_data = {"Measurements": [(1.1, 2.3), (1.9, 3.1), (3.2, 4.0), (4.5, 5.1)]}
    chart = ui.ScatterPlot(data=scatter_data, title="Height vs. Weight")
    
    def randomize_data():
        new_data = {"Measurements": [(random.uniform(1,5), random.uniform(2,6)) for _ in range(4)]}
        chart.set_data(new_data)

    return ui.Column([chart, ui.Button("Randomize", on_click=randomize_data)])

# To run this, you would need a WinUp app instance.
# Example: winup.run(main_component_path="graph_demo:App", title="Scatter Plot Demo")
```

## Slider
The `Slider` widget provides a highly customizable slider control. You can control its range, step, initial value, and appearance.

*   `min`, `max`: The minimum and maximum values of the slider.
*   `step`: The increment for each step of the slider.
*   `value`: The initial value of the slider.
*   `track_color`: The color of the slider's track (the groove).
*   `thumb_style`: A dictionary of CSS-like properties to style the slider's handle (the thumb).

```python
import winup
from winup import ui

def App():
    label = ui.Label("Slider Value: 50")

    def update_label(value):
        label.set_text(f"Slider Value: {value}")

    slider = ui.Slider(
        min=0,
        max=100,
        step=5,
        value=50,
        on_change=update_label,
        track_color="#a9def9",
        thumb_style={
            "background-color": "#1a73e8",
            "border-radius": "10px"
        }
    )

    return ui.Column([label, slider], props={"spacing": 10, "padding": "20px"})

# Example: winup.run(main_component_path="slider_demo:App", title="Slider Demo")
```