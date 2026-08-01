"""
This file contains the ArduinoListener class, to help listen to 
incomming signals.
"""

from PySide6.QtCore import QObject, Signal 
from pyfirmata2 import Arduino

class AruinoListener(QObject):

    signal = Signal(str, object)

    def __init__(self, auto_detect: bool=True, port: str=None, sampling_rate: int=500):
        super().__init__()

        if auto_detect:
            self.port = Arduino.AUTODETECT
        else: self.port = port 

        self._sampling_rate = sampling_rate
        self._signals = {}

        self.board = Arduino(self.port)
        self.board.samplingOn(self._sampling_rate)  

    @property
    def sampling_rate(self): return self._sampling_rate
    
    @sampling_rate.setter 
    def sampling_rate(self, new_rate: int):
        self._sampling_rate = new_rate
        self.board.samplingOn(self._sampling_rate)

    def add_signal(self, name: str, callback):
        self._signals[name] = callback

    def emit_signal(self, name: str, value: object):
        if name in self._signals: self._signals[name](value)
        self.signal.emit(name, value)

    def sampling_off(self): self.board.samplingOff()    