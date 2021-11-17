import random
from typing import AnyStr, List

from PyQt5.QtCore import QObject, QRunnable,  pyqtSignal, pyqtSlot


class MorseTranslatorSignals(QObject):
    """Defines the signals available from a running MorseTranslator thread."""
    morse_code = pyqtSignal(str)
    translated_morse_code = pyqtSignal(str)
    collected_arduino_data = pyqtSignal(bytes)


class MorseTranslator(QRunnable):

    def __init__(self, unit_length: int = 1):
        super(MorseTranslator, self).__init__()

        self.unit_length = unit_length
        self.continue_run = True
        self.signals = MorseTranslatorSignals()
        self.arduino_data: List[AnyStr] = []

    @pyqtSlot()
    def run(self):
        self.translate()

    def translate(self):
        while self.continue_run:
            ...
        # TODO Call transform functions

        self.signals.morse_code.emit(str(self.arduino_data))
        self.signals.translated_morse_code.emit(str(self.arduino_data))

    def stop_translation(self):
        self.continue_run = False  # set the run condition to false on stop_translation

    def catch_arduino_data(self, arduino_data):
        print(arduino_data)
        # self.arduino_data.append(arduino_data)
        self.arduino_data.append(str(random.random()))
        #

