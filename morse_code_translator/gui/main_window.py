import webbrowser
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from morse_code_translator.gui.intro_window import IntroWindow


class UiMainWindow(object):
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

        self.morse_code_text = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.morse_code_text.setFont(font)
        self.morse_code_text.setReadOnly(False)
        self.morse_code_text.setObjectName("morse_code_text")
        self.text_vertical_layout.addWidget(self.morse_code_text)

        self.translated_morse_code_text = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
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
        _translate = QtCore.QCoreApplication.translate
        self.start_window.setWindowTitle(_translate("main_window", "main_window"))
        self.title.setText(_translate("main_window", "Morse code translator"))
        self.footer.setText(_translate("main_window",
                                       "<html><head/><body><p align=\"center\">Michał Kacprzak &amp; Jakub Strugała</p><p align=\"center\">Komputeryzacja pomiarów 2021, Wydział Fizyki i Informatyki Stosowanej</p></body></html>"))
        self.morse_code_text.setHtml(_translate("main_window",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Morse code</p></body></html>"))
        self.translated_morse_code_text.setHtml(_translate("main_window",
                                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                           "p, li { white-space: pre-wrap; }\n"
                                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Translated morse code</span></p></body></html>"))
        self.start_stop_button.setText(_translate("main_window", "Start"))

        self.unit_length_select.setItemText(0, _translate("main_window", "Select unit length in seconds"))
        self.unit_length_select.setItemText(1, _translate("main_window", "1"))
        self.unit_length_select.setItemText(2, _translate("main_window", "2"))
        self.unit_length_select.setItemText(3, _translate("main_window", "5"))
        self.unit_length_select.setItemText(4, _translate("main_window", "10"))

        self.analyze_button.setText(_translate("main_window", "Analyze"))
        self.instruction_button.setText(_translate("main_window", "Instruction"))


class MainWindow(UiMainWindow):
    def __init__(self, start_window):
        self.setupUi(start_window)
        self.window = QtWidgets.QMainWindow()
        self.intro_window = IntroWindow(self.window, start_window)
        self.start_window.hide()

        self.image_editor_window = None

        self.instruction_button.clicked.connect(self.show_instruction)
        self.start_stop_button.clicked.connect(self.start_translation)

    def start_translation(self):
        _translate = QtCore.QCoreApplication.translate
        if self.start_stop_button.text() == "Start":
            self.start_stop_button.setText(_translate("main_window", "Stop"))
            self.morse_code_text.setText(_translate("main_window", ""))
            self.translated_morse_code_text.setText(_translate("main_window", ""))
        else:
            self.start_stop_button.setText(_translate("main_window", "Start"))

    def show_instruction(self):
        current_dir = Path(__file__).parent
        webbrowser.open_new(current_dir / "../project_description/AO_dokumentacja_projektu.pdf")

    def hide_window(self):
        self.intro_window.intro_window.show()

    def start(self):
        self.intro_window.start()
