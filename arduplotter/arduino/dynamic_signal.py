"""
This file contains the dynmaic signal class
"""

from PySide6.QtCore import QObject, Signal

class DynamicSignal(QObject):
    SIGNAL = Signal(object)

    def __init__(self): super().__init__()