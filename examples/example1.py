"""
A simple example of how you can use arduplotter to plot a voltage reading from a potentiometer
connected to analog port 0 on the Arduino.
"""
from PySide6.QtWidgets import QApplication, QMainWindow
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

def main():
    app = QApplication()
    ardu = ArduinoListener()
   
    window = MyWindow()
    window.show()

    start_time = 0 

    def process_data(value):
        time_passed = (time.time() - start_time) * 1000
        voltage = value * 5 
        ardu.emit_signal("voltage_data", (time_passed, voltage))

    ardu.configure_analog_pin_for_reporting(pin_number=0, callback=process_data)

    ardu.add_signal("voltage_data", window.chart_callback)
    
    start_time = time.time()
    ardu.start_sampling()

    app.exec()
    ardu.quit()

if __name__ == "__main__":
    main()