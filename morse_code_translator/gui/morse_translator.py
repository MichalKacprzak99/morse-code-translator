from PyQt5.QtCore import QObject, QRunnable, QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtCore


class ModelSignals(QObject):
    """Defines the signals available from a running worker thread."""
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    morse_code = pyqtSignal(str)
    translated_morse_code = pyqtSignal(str)


class MorseTranslator(QRunnable):
    trained_model = None

    def __init__(self, unit_length: int):
        super(MorseTranslator, self).__init__()

        self.unit_length = unit_length
        self.continue_run = True
        self.signals = ModelSignals()

    def predict(self, img):
        return self.trained_model.predict(img)

    @pyqtSlot()
    def run(self):
        _translate = QtCore.QCoreApplication.translate
        i = 1
        while self.continue_run:  # give the loop a stoppable condition
            QThread.sleep(1)
            i = i + 1
            self.signals.morse_code.emit(str(i))
            self.signals.translated_morse_code.emit(str(i))
        self.signals.finished.emit()  # Done

    def stop(self):
        self.continue_run = False  # set the run condition to false on stop
