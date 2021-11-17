import serial

from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class ArduinoDataCollectorSignals(QObject):
    """Defines the signals available from a running ArduinoDataCollector thread."""
    collected_arduino_data = pyqtSignal(bytes)


class ArduinoDataCollector(QObject):

    def __init__(self, arduino_port: str, arduino_baudrate: int):
        super().__init__()
        self._arduino = serial.Serial()
        self._arduino.baudrate = arduino_baudrate
        self._arduino.port = arduino_port
        self.signals = ArduinoDataCollectorSignals()
        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(self.collect_arduino_data)

    def start(self):
        # self._arduino.open()
        self._timer.start(100)

    def stop(self):
        # self._arduino.close()
        self._timer.stop()

    def collect_arduino_data(self):
        # self.collected_arduino_data.emit(self._arduino.read(1))
        self.signals.collected_arduino_data.emit(bytes(1))
