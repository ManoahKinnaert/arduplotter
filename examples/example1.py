from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QLabel
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy

from arduplotter.arduino import ArduinoListener
from arduplotter.plots import ChartWidget

import time

class MyWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Plotting example")
        self.setMinimumSize(800, 600)

        self.chart = ChartWidget(5, 4, 100)
        self.chart.add_subplot("potentiometer", "PotentiometerVoltage", "Time (ms)", "Voltage (V)", 111)
        self.chart.add_line_plot("potentiometer", 10)
       
        self.setCentralWidget(self.chart)

    def chart_callback(self, data):
        self.chart.update_data("potentiometer", data[0], data[1])

class ArduListener(ArduinoListener):
    def __init__(self):
        super().__init__()

        self.A0 = self.board.analog[0]
        self.start_time = time.time()

        # register callback
        self.A0.register_callback(self.process_data)
        self.A0.enable_reporting()

    def process_data(self, value):
        time_passed = (time.time() - self.start_time) * 1000
        voltage = value * 5
        self.emit_signal("voltage_data", (time_passed, voltage)) 


def main():
    app = QApplication()

    window = MyWindow()
    window.show()

    ardu = ArduListener()
    ardu.add_signal("voltage_data", window.chart_callback)

    app.exec()


if __name__ == "__main__":
    main()