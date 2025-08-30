from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QScatterSeries
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt
from .... import style

class ScatterPlot(QWidget):
    """A stylish, modern scatter plot widget."""
    def __init__(self, data: dict = None, title: str = "", props: dict = None, parent=None):
        super().__init__(parent)

        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundBrush(QColor("transparent"))
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        if props:
            style.styler.apply_props(self, props)

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
        Sets the data for the scatter plot.
        Data should be a dictionary where keys are series names and values are lists of (x, y) points.
        Example: {"Observations": [(1, 5), (3.5, 7.2), (4.8, 6.1)]}
        """
        self.chart.removeAllSeries()
        
        for series_name, points in data.items():
            series = QScatterSeries()
            series.setName(series_name)
            for point in points:
                series.append(point[0], point[1])
            self.chart.addSeries(series)

        self.chart.createDefaultAxes() 