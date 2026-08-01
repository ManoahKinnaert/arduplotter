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
       
        self._setup_ui()

    def chart_callback(self, data):
        self.chart.update_data("potentiometer", data[0], data[1])

    def _setup_ui(self):
        mylayout = QVBoxLayout()

        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.Shape.NoFrame)
        body_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding) 
        mylayout.addWidget(body_frame)

        chart_layout = QVBoxLayout()
        chart_layout.addWidget(self.chart)
        body_frame.setLayout(chart_layout)

        central_widget = QWidget()
        central_widget.setLayout(mylayout)
        self.setCentralWidget(central_widget)

class ArduListener(ArduinoListener):
    def __init__(self):
        super().__init__()

        self.A0 = self.board.analog[0]
        self.start_time = time.time()

        # register callback
        self.A0.register_callback(self.plot_data)
        self.A0.enable_reporting()



    def plot_data(self, value):
        time_passed = (time.time() - self.start_time) * 1000
        self.emit_signal("voltage_data", (time_passed, value * 5)) 


def main():
    app = QApplication()

    window = MyWindow()
    window.show()

    ardu = ArduListener()
    ardu.add_signal("voltage_data", window.chart_callback)
    app.exec()


if __name__ == "__main__":
    main()