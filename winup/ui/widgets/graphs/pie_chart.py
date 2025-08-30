from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt
from .... import style

class PieChart(QWidget):
    """A stylish, modern pie chart widget, rendered as a donut chart."""
    def __init__(self, data: dict = None, title: str = "", props: dict = None, parent=None):
        super().__init__(parent)

        self.series = QPieSeries()
        self.series.setHoleSize(0.35) # Donut chart style

        if data:
            self.set_data(data)
        
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(title)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundBrush(QColor("transparent"))
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        if props:
            style.styler.apply_props(self, props)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def set_data(self, data: dict):
        """
        Sets the data for the pie chart.
        Data should be a dictionary where keys are slice labels and values are numbers.
        Example: {"Apples": 5, "Oranges": 8, "Bananas": 3}
        """
        self.series.clear()
        for label, value in data.items():
            slice_ = self.series.append(label, value)
            slice_.setLabelVisible(True) 