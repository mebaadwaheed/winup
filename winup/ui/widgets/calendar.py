from PySide6.QtWidgets import QCalendarWidget
import datetime

class Calendar(QCalendarWidget):
    def __init__(self, parent=None, props: dict = None):
        super().__init__(parent)
        self.setStyleSheet("""
            QCalendarWidget QToolButton {
                height: 30px;
                width: 150px;
                color: white;
                font-size: 14px;
                icon-size: 20px, 20px;
                background-color: #007BFF;
            }
            QCalendarWidget QMenu {
                width: 150px;
                left: 20px;
                color: white;
                font-size: 12px;
                background-color: #007BFF;
            }
            QCalendarWidget QSpinBox { 
                width: 150px; 
                font-size:14px; 
                color: white; 
                background-color: #007BFF; 
                selection-background-color: #007BFF;
                selection-color: rgb(255, 255, 255);
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size:12px;  
                color: #2a2a2a;  
                background-color: white;  
                selection-background-color: #007BFF; 
                selection-color: white; 
            }
        """)

        if props:
            style.apply_props(self, props)
        
        self.props = props

    def set_date(self, date: datetime.date):
        self.setSelectedDate(date)
