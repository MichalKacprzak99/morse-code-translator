import random
from typing import AnyStr, List

import serial
from PyQt5.QtCore import QObject, QRunnable,  pyqtSignal, pyqtSlot, QTimer


class ArduinoDataCollector(QObject):
    finished = pyqtSignal()
    collected_arduino_data = pyqtSignal(bytes)

    def __init__(self, arduino_port: str, arduino_baudrate: int):
        super().__init__()
        self.arduino = serial.Serial()
        self.arduino.baudrate = arduino_baudrate
        self.arduino.port = arduino_port

    def start(self):
        # self.arduino.open()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.collect_arduino_data)
        self._timer.start(100)

    def stop(self):
        # self.arduino.close()
        self._timer.stop()
        self.finished.emit()

    def collect_arduino_data(self):
        # self.collected_arduino_data.emit(self.arduino.read(1))
        self.collected_arduino_data.emit(bytes(1))


class MorseTranslatorSignals(QObject):
    """Defines the signals available from a running MorseTranslator thread."""
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
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
        self.signals.finished.emit()  # Done

    def translate(self):
        while self.continue_run:
            ...
        # TODO Call transform functions

        self.signals.morse_code.emit(str(self.arduino_data))
        self.signals.translated_morse_code.emit(str(self.arduino_data))

    def stop_translation(self):
        self.continue_run = False  # set the run condition to false on stop_translation

    def read_arduino(self, translated_char):
        print(translated_char)
        self.arduino_data.append(str(random.random()))
        #

