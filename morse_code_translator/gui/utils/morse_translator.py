import random
from typing import AnyStr, List

from PyQt5.QtCore import QObject, pyqtSignal

from morse_code_translator.decryption_algorithm.algorithm import convert_from_arduino_to_morse
from morse_code_translator.decryption_algorithm.morse_code_translation import decrypt_from_morse


class MorseTranslatorSignals(QObject):
    """Defines the signals available for MorseTranslator object"""
    morse_code = pyqtSignal(str)
    translated_morse_code = pyqtSignal(str)
    collected_arduino_data = pyqtSignal(bytes)


class MorseTranslator(QObject):

    def __init__(self):
        super().__init__()
        self.signals = MorseTranslatorSignals()
        self._arduino_data: List[AnyStr] = []

    def translate(self, unit_length):
        # TODO pass unit_length to convert_from_arduino_to_morse
        # TODO Uncomment when connected with arduino
        # morse_code_from_arduino = convert_from_arduino_to_morse(''.join(self._arduino_data))
        # translated_morse_code = decrypt_from_morse(morse_code_from_arduino)
        # self.signals.morse_code.emit(morse_code_from_arduino)
        # self.signals.translated_morse_code.emit(translated_morse_code)
        self.signals.morse_code.emit(str(self._arduino_data))
        self.signals.translated_morse_code.emit(str(self._arduino_data))

    def catch_arduino_data(self, arduino_data):
        print(arduino_data)
        # self._arduino_data.append(_arduino_data)
        self._arduino_data.append(str(random.random()))
