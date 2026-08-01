"""
This file contains the ArduinoListener class, to help listen to 
incomming signals.
"""

from PySide6.QtCore import QObject, Signal 
from pyfirmata2 import Arduino

from .dynamic_signal import DynamicSignal

class ArduinoListener(QObject):
    def __init__(self, auto_detect: bool=True, port: str=None, sampling_rate: int=500):
        super().__init__()

        if auto_detect:
            self.port = Arduino.AUTODETECT
        else: 
            if port is None: raise ValueError("When entering a manual port, the port can't be None!") 
            self.port = port 

        self._sampling_rate = sampling_rate
        self._signals = {}

        self.board = Arduino(self.port)
        self.board.samplingOn(self._sampling_rate)  

    @property
    def sampling_rate(self): return self._sampling_rate

    @property 
    def signals(self): return self._signals.copy()
    
    @sampling_rate.setter 
    def sampling_rate(self, new_rate: int):
        self._sampling_rate = new_rate
        self.board.samplingOn(self._sampling_rate)

    def add_signal(self, name: str, callback):
        dyn_signal = DynamicSignal()
        dyn_signal.SIGNAL.connect(callback)
        self._signals[name] = dyn_signal

    def emit_signal(self, name: str, value: object):
        if name in self._signals: self._signals[name].emit(value)

    def sampling_off(self): self.board.samplingOff()    