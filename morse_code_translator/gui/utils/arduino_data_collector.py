from typing import Optional

import serial
from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class ArduinoDataCollector(QObject):
    finished = pyqtSignal()
    collected_arduino_data = pyqtSignal(bytes)

    def __init__(self, arduino_port: str, arduino_baudrate: int):
        super().__init__()
        self._arduino = serial.Serial()
        self._arduino.baudrate = arduino_baudrate
        self._arduino.port = arduino_port

        self._timer: Optional[QTimer] = None

    def start(self):
        # self._arduino.open()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.collect_arduino_data)
        self._timer.start(100)

    def stop(self):
        # self._arduino.close()
        self._timer.stop()
        self.finished.emit()

    def collect_arduino_data(self):
        # self.collected_arduino_data.emit(self._arduino.read(1))
        self.collected_arduino_data.emit(bytes(1))
