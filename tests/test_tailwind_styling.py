import unittest
from PySide6.QtWidgets import QApplication
from winup.ui.widgets.button import Button
from winup.style.styler import styler

class TestTailwindStyling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a QApplication instance for testing
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()

    def test_desktop_tailwind_styling(self):
        # Arrange
        tailwind_props = "bg-blue-500 text-white p-4"
        expected_qss = "background-color: #3B82F6;color: #FFFFFF;padding: 16px;"

        # Act
        props = {'tailwind': tailwind_props}
        button = Button(props=props)
        styler.apply_props(button, props)

        # Assert
        self.assertIn(expected_qss.replace(" ", ""), button.styleSheet().replace(" ", ""))

if __name__ == '__main__':
    unittest.main()
