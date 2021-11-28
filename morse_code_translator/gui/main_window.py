import os
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from .intro_window import IntroWindow
from .utils import ArduinoDataCollector, MorseTranslator


class UiMainWindow(QObject):
    def setupUi(self, main_window):
        self.start_window = main_window
        self.start_window.setObjectName("main_window")
        self.start_window.resize(1104, 854)

        self.central_widget = QtWidgets.QWidget(self.start_window)
        self.central_widget.setObjectName("central_widget")

        self.title = QtWidgets.QLabel(self.central_widget)
        self.title.setGeometry(QtCore.QRect(10, 0, 1077, 81))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")

        self.footer = QtWidgets.QLabel(self.central_widget)
        self.footer.setGeometry(QtCore.QRect(10, 740, 1077, 81))
        self.footer.setWordWrap(False)
        self.footer.setObjectName("footer")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.central_widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 180, 621, 361))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.text_vertical_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.text_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.text_vertical_layout.setObjectName("text_vertical_layout")

        font = QtGui.QFont()
        font.setPointSize(16)

        self.morse_code_text = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.morse_code_text.setFont(font)
        self.morse_code_text.setReadOnly(False)
        self.morse_code_text.setObjectName("morse_code_text")
        self.text_vertical_layout.addWidget(self.morse_code_text)

        self.translated_morse_code_text = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.translated_morse_code_text.setFont(font)
        self.translated_morse_code_text.setObjectName("translated_morse_code_text")
        self.text_vertical_layout.addWidget(self.translated_morse_code_text)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(760, 180, 287, 361))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.config_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        self.config_layout.setObjectName("config_layout")

        self.start_stop_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.start_stop_button.setFont(font)
        self.start_stop_button.setObjectName("start_stop_button")
        self.config_layout.addWidget(self.start_stop_button)

        self.select_error = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.select_error.setGeometry(QtCore.QRect(50, 60, 200, 81))
        self.select_error.hide()
        self.select_error.setObjectName("footer")

        self.unit_length_select = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.unit_length_select.setFont(font)
        self.unit_length_select.setPlaceholderText("")
        self.unit_length_select.setObjectName("unit_length_select")
        self.unit_length_select.addItem("")
        self.unit_length_select.addItem("")
        self.unit_length_select.addItem("")
        self.unit_length_select.addItem("")
        self.unit_length_select.addItem("")
        self.config_layout.addWidget(self.unit_length_select)

        self.analyze_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.analyze_button.setFont(font)
        self.analyze_button.setObjectName("analyze_button")
        self.config_layout.addWidget(self.analyze_button)

        self.instruction_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.instruction_button.setFont(font)
        self.instruction_button.setObjectName("instruction_button")
        self.config_layout.addWidget(self.instruction_button)

        self.start_window.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(self.start_window)
        self.statusbar.setObjectName("statusbar")
        self.start_window.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.start_window)

    def retranslateUi(self):
        self.translate = QtCore.QCoreApplication.translate
        self.start_window.setWindowTitle(self.translate("main_window", "main_window"))
        self.title.setText(self.translate("main_window", "Morse code translator"))
        self.select_error.setText(
            self.translate("main_window", "<font color='red'>Error! Please select unit length!</font>"))
        self.footer.setText(
            "<html>"
            "<head/>"
            "<body>"
            "<p align=\"center\">Michał Kacprzak &amp; Jakub Strugała</p>"
            "<p align=\"center\">Komputeryzacja pomiarów 2021, Wydział Fizyki i Informatyki Stosowanej</p>"
            "</body>"
            "</html>")
        self.morse_code_text.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html>"
            "<head>"
            "<meta name=\"qrichtext\" content=\"1\" />"
            "<style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style>"
            "</head>"
            "<body style=\" font-family:\'MS Shell Dlg 2\'; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Morse code</p>"
            "</body>"
            "</html>")
        self.translated_morse_code_text.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html>"
            "<head>"
            "<meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style>"
            "</head>"
            "<body style=\" font-family:\'MS Shell Dlg 2\'; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Translated morse code</p>"
            "</body>"
            "</html>")

        self.start_stop_button.setText(self.translate("main_window", "Start"))

        self.unit_length_select.setItemText(0, self.translate("main_window", "Select unit length in seconds"))
        self.unit_length_select.setItemText(1, self.translate("main_window", "1"))
        self.unit_length_select.setItemText(2, self.translate("main_window", "2"))
        self.unit_length_select.setItemText(3, self.translate("main_window", "5"))
        self.unit_length_select.setItemText(4, self.translate("main_window", "10"))

        self.analyze_button.setText(self.translate("main_window", "Analyze"))
        self.instruction_button.setText(self.translate("main_window", "Instruction"))


class MainWindow(UiMainWindow):
    stop_simulation_signal = pyqtSignal()

    def __init__(self, start_window):
        super().__init__()
        self.setupUi(start_window)
        self.window = QtWidgets.QMainWindow()
        self.intro_window = IntroWindow(self.window, start_window)
        self.start_window.hide()

        self.instruction_button.clicked.connect(self.show_instruction)
        self.start_stop_button.clicked.connect(self.handle_translation)
        self.unit_length_select.currentIndexChanged.connect(self.on_unit_length_select_change)
        self.analyze_button.clicked.connect(self.visualize_translation_statistics)

        self.morse_translator = MorseTranslator()
        self.morse_translator.signals.translated_morse_code.connect(self._update_translated_morse_code_text)
        self.morse_translator.signals.morse_code.connect(self._update_morse_code_text)

        self.thread = QThread()
        self.arduino_data_collector = ArduinoDataCollector(arduino_port='COM6', arduino_baudrate=9600)
        self.arduino_data_collector.signals.collected_arduino_data.connect(self.morse_translator.catch_arduino_data)
        self.arduino_data_collector.moveToThread(self.thread)
        self.thread.started.connect(self.arduino_data_collector.start)

    def handle_translation(self):
        if self.start_stop_button.text() == "Start":
            self._start_translation()
        else:
            self._stop_translation()

    def _start_translation(self):
        if self.unit_length_select.currentIndex() != 0:
            self.start_stop_button.setText(self.translate("main_window", "Stop"))
            self.morse_code_text.setHtml("Morse code")
            self.translated_morse_code_text.setHtml("Translated morse code")

            self.thread.start()
        else:
            self.select_error.show()

    def _stop_translation(self):
        self.start_stop_button.setText(self.translate("main_window", "Start"))
        self.morse_code_text.setHtml(self.translate("main_window", ""))
        self.translated_morse_code_text.setHtml(self.translate("main_window", ""))

        self.arduino_data_collector.stop()

        unit_length = self.unit_length_select.currentText()
        self.morse_translator.translate(int(unit_length))

        self.thread.quit()
        self.thread.wait()

    def _update_morse_code_text(self, morse_code_sign):
        self.morse_code_text.setHtml(self.translate("main_window", morse_code_sign))

    def _update_translated_morse_code_text(self, translated_char):
        self.translated_morse_code_text.setHtml(self.translate("main_window", translated_char))

    def on_unit_length_select_change(self, index):
        if index != 0:
            self.select_error.hide()

    @staticmethod
    def show_instruction():
        instruction_path = Path(__file__).parents[2] / "prezi/AGH_prezentacja_3_2.pptx"
        os.startfile(instruction_path)

    def visualize_translation_statistics(self):
        save_statistics_to = QtWidgets.QFileDialog.getExistingDirectory(self.start_window)
        self.morse_translator.visualize_translation_statistics(save_statistics_to=Path(save_statistics_to))

    def start_application(self):
        self.intro_window.start()
