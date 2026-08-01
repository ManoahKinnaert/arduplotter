"""
This file contains the ArduinoListener class, to help listen to 
incoming signals.
"""

from PySide6.QtCore import QObject  
from pyfirmata2 import Arduino, Pin

from .dynamic_signal import DynamicSignal


class ArduinoListener(QObject):
    """
    An arduino listener class, to help listen to incomming signals.
    It also helps with gui callback function so we can dynamically update our charts.
    """
    def __init__(self, auto_detect: bool=True, port: str=None, sampling_rate: int=500):
        """
        ==== Arguments ====
        auto_detect: bool -> do we want to autodetect the arduino board or not, 
        by default set to True

        port: str -> by default None because we want to autodetect, if not it can't be None and must
        be of type str

        sampling_rate: int -> an integer representing the sampling rate of the board in miliseconds,
        it is equal to 500ms by default
        """
        super().__init__()

        if auto_detect:
            self.port = Arduino.AUTODETECT
        else: 
            if port is None: raise ValueError("When entering a port manually, the port can't be None!") 
            self.port = port 

        self._sampling_rate = sampling_rate
        self._signals = {}

        self.board = Arduino(self.port)

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
        if name in self._signals: self._signals[name].SIGNAL.emit(value)

    def start_sampling(self): self.board.samplingOn(self._sampling_rate)

    def sampling_off(self): self.board.samplingOff()

    def quit(self): self.board.exit()

    def list_analog_pins(self): return self.board.analog.copy()

    def list_digital_pins(self): return self.board.digital.copy()

    def get_analog_pin(self, number: int): return self.board.analog[number]

    def get_digital_pin(self, number: int): return self.board.digital[number]

    @staticmethod
    def pin_supports_pwm(pin: Pin): return pin.PWM_CAPABLE