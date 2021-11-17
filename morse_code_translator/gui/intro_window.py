from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QFont
from .custom_elements import FontChangeableLabel
import numpy as np


class UiIntroWindow(object):
    def setupUi(self, intro_window):
        self.intro_window = intro_window
        self.intro_window.setObjectName("intro_window")
        self.intro_window.setStyleSheet("background:white")
        self.intro_window.resize(629, 619)
        self.central_widget = QtWidgets.QWidget(intro_window)
        self.central_widget.setObjectName("central_widget")

        self.intro_image = QtWidgets.QLabel(self.central_widget)
        self.intro_image.setGeometry(QtCore.QRect(0, 0, 629, 619))
        self.intro_image.setText("")
        current_dir = Path(__file__).parent
        self.intro_image.setPixmap(QtGui.QPixmap(str((current_dir / "resources/morse_code_project_logo.png"))))
        self.intro_image.setObjectName("intro_image")

        self.intro_label = FontChangeableLabel(self.central_widget)
        self.intro_label.setGeometry(QtCore.QRect(180, 560, 271, 41))
        self.intro_label.setAlignment(QtCore.Qt.AlignCenter)
        self.intro_label.setObjectName("intro_label")

        self.go_further_button = QtWidgets.QPushButton(self.central_widget)
        self.go_further_button.setGeometry(QtCore.QRect(0, -5, 629, 619))
        self.go_further_button.setText("")
        self.go_further_button.setFlat(True)
        self.go_further_button.setObjectName("go_further_button")

        self.intro_window.setCentralWidget(self.central_widget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(intro_window)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.intro_window.setWindowTitle(_translate("intro_window", "MainWindow"))
        self.intro_label.setText(_translate("intro_window", "Click to continue"))
        self.intro_label.setFont(QFont('Arial', 1))


class IntroWindow(UiIntroWindow):
    def __init__(self, window, start_window):
        self.start_window = start_window
        self.animation = None
        self.setupUi(window)
        self.transform_text()
        self.go_further_button.clicked.connect(self.close_window)

    def close_window(self):
        self.intro_window.close()
        self.start_window.show()

    def transform_text(self):
        self.animation = QPropertyAnimation(self.intro_label, b"font")
        self.animation.setDuration(8000)
        self.animation.setStartValue(5)
        time_frames = np.linspace(0, 1, num=20)
        font_sizes = [i for i in range(5, 15)] + [i for i in range(15, 5, -1)]
        for time_frame, font_size in zip(time_frames, font_sizes):
            self.animation.setKeyValueAt(time_frame, font_size)
        self.animation.setEndValue(5)
        self.animation.setLoopCount(-1)
        self.animation.start()

    def start(self):
        self.intro_window.show()
