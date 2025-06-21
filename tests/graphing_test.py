import winup
from winup import ui, state
import random

# --- Helper Functions for Data Generation ---

def generate_bar_data():
    """Generates random data for the bar chart."""
    categories = ["Alpha", "Bravo", "Charlie", "Delta", "Echo"]
    return {cat: random.randint(10, 100) for cat in categories}

def generate_line_data():
    """Generates random data for the line chart."""
    return {
        "Series 1": [(i, random.uniform(20, 40)) for i in range(10)],
        "Series 2": [(i, random.uniform(50, 70)) for i in range(10)]
    }

def generate_pie_data():
    """Generates random data for the pie chart."""
    return {
        "Product A": random.randint(5, 30),
        "Product B": random.randint(10, 40),
        "Product C": random.randint(20, 50)
    }

def generate_scatter_data():
    """Generates random data for the scatter plot."""
    return {
        "Cluster 1": [(random.uniform(0, 5), random.uniform(0, 5)) for _ in range(20)],
        "Cluster 2": [(random.uniform(5, 10), random.uniform(5, 10)) for _ in range(20)]
    }

# --- Tab Creation Functions ---

def create_bar_chart_tab():
    """Creates the UI for the Bar Chart demo tab."""
    chart = ui.BarChart(data=generate_bar_data(), title="Sample Bar Chart")
    return ui.Column(props={"spacing": 10}, children=[
        chart,
        ui.Button("Randomize Data", on_click=lambda: chart.set_data(generate_bar_data()))
    ])

def create_line_chart_tab():
    """Creates the UI for the Line Chart demo tab."""
    chart = ui.LineChart(data=generate_line_data(), title="Sample Line Chart")
    return ui.Column(props={"spacing": 10}, children=[
        chart,
        ui.Button("Randomize Data", on_click=lambda: chart.set_data(generate_line_data()))
    ])

def create_pie_chart_tab():
    """Creates the UI for the Pie Chart demo tab."""
    chart = ui.PieChart(data=generate_pie_data(), title="Sample Pie Chart")
    return ui.Column(props={"spacing": 10}, children=[
        chart,
        ui.Button("Randomize Data", on_click=lambda: chart.set_data(generate_pie_data()))
    ])

def create_scatter_plot_tab():
    """Creates the UI for the Scatter Plot demo tab."""
    chart = ui.ScatterPlot(data=generate_scatter_data(), title="Sample Scatter Plot")
    return ui.Column(props={"spacing": 10}, children=[
        chart,
        ui.Button("Randomize Data", on_click=lambda: chart.set_data(generate_scatter_data()))
    ])

# --- Main Application ---

def App():
    """The main app uses a TabView to organize the chart demos."""
    return ui.TabView(tabs={
        "Bar Chart": create_bar_chart_tab(),
        "Line Chart": create_line_chart_tab(),
        "Pie Chart": create_pie_chart_tab(),
        "Scatter Plot": create_scatter_plot_tab(),
    })

if __name__ == "__main__":
    winup.run(
        main_component_path="graphing_test:App",
        title="Graphing Widgets Demo",
        width=800,
        height=600
    )