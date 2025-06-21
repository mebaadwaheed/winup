from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class BarChart(QWidget):
    """A stylish, modern bar chart widget."""
    def __init__(self, data: dict = None, title: str = "", parent=None):
        super().__init__(parent)

        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundBrush(QColor("transparent"))
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.series = QBarSeries()
        
        if data:
            self.set_data(data)

        self.chart.addSeries(self.series)

        # Axis setup
        self.axis_x = QBarCategoryAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def set_data(self, data: dict):
        """
        Sets the data for the bar chart.
        Data should be a dictionary where keys are categories and values are numbers.
        Example: {"Apples": 5, "Oranges": 8, "Bananas": 3}
        """
        self.series.clear()
        categories = list(data.keys())
        bar_set = QBarSet("Values")
        bar_set.append(list(data.values()))
        self.series.append(bar_set)
        
        if hasattr(self, 'axis_x'):
            self.axis_x.clear()
            self.axis_x.append(categories)
            
        if hasattr(self, 'axis_y') and data:
            max_val = max(data.values()) if data.values() else 0
            self.axis_y.setRange(0, max_val * 1.1 if max_val > 0 else 10) 