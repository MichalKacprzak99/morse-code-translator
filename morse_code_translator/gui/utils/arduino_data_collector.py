import serial

from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class ArduinoDataCollectorSignals(QObject):
    """Defines the signals available from a running ArduinoDataCollector thread."""
    collected_arduino_data = pyqtSignal(bytes)


class ArduinoDataCollector(QObject):

    def __init__(self, arduino_port: str, arduino_baudrate: int):
        super().__init__()
        self._arduino = serial.Serial(arduino_port, arduino_baudrate)
        self.signals = ArduinoDataCollectorSignals()
        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(self.collect_arduino_data)

    def start(self):
        self._timer.start(100)

    def stop(self):
        self._timer.stop()

    def collect_arduino_data(self):
        arduino_data = self._arduino.read(1)
        self.signals.collected_arduino_data.emit(arduino_data)
