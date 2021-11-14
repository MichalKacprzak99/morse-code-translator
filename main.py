import glob
import sys

import serial

from PyQt5 import QtWidgets

from morse_code_translator.gui import MainWindow as MorseTranslatorApp


def read_arduino(arduino):
    for _ in range(10):
        arduino.read(30)


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    # print(serial_ports())
    # arduino = serial.Serial('COM4', 9600)
    # time.sleep(1)
    # while True:
    #     time.sleep(0.1)
    #     print(str(arduino.read(1), "utf-8"))
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    morse_translator_app = MorseTranslatorApp(window)
    morse_translator_app.start_application()
    sys.exit(app.exec_())
