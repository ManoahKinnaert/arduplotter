from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QLabel
from arduplotter.arduino import ArduinoListener
from arduplotter.plots import ChartWidget

import time

START_TIME = time.time()
ARDU = ArduinoListener()
INPUT = ARDU.board.analog[0]

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


def process_data(value):
    time_passed = (time.time() - START_TIME) * 1000
    voltage = value * 5 
    ARDU.emit_signal("voltage_data", (time_passed, voltage))

def main():
    app = QApplication()

    window = MyWindow()
    window.show()

    INPUT.register_callback(process_data)
    INPUT.enable_reporting()

    ARDU.add_signal("voltage_data", window.chart_callback)
    ARDU.start_sampling()

    app.exec()
    ARDU.quit()

if __name__ == "__main__":
    main()