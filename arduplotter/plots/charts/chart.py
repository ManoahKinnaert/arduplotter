from abc import ABC, abstractmethod

class Chart(ABC):
    def __init__(self, axes, datapoint_limit=None):
        self.axes = axes
        self.datapoint_limit = datapoint_limit

    @abstractmethod
    def update(self, x, y):
        """Update the chart with a new data point."""