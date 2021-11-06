from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class CustomLabel(QLabel):
    def __init__(self, parent, name=""):
        super().__init__(name, parent)
        self._font = self.fontInfo().pointSize()

    @pyqtProperty(int)
    def font(self):
        return self.fontInfo().pointSize()

    @font.setter
    def font(self, value):
        self.setFont(QFont('Arial', value))