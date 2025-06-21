from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class LineChart(QWidget):
    """A stylish, modern line chart widget."""
    def __init__(self, data: dict = None, title: str = "", parent=None):
        super().__init__(parent)

        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundBrush(QColor("transparent"))
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        if data:
            self.set_data(data)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def set_data(self, data: dict):
        """
        Sets the data for the line chart.
        Data should be a dictionary where keys are series names and values are lists of (x, y) points.
        Example: {"Series 1": [(0, 6), (2, 4), (3, 8), (7, 4), (10, 5)]}
        """
        self.chart.removeAllSeries()
        
        for series_name, points in data.items():
            series = QLineSeries()
            series.setName(series_name)
            for point in points:
                series.append(point[0], point[1])
            self.chart.addSeries(series)

        self.chart.createDefaultAxes() 