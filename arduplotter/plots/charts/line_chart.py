from .chart import Chart 

class LineChart(Chart):
    def __init__(self, axes, datapoint_limit=None, **kwargs):
        super().__init__(axes, datapoint_limit)

        self._line, = axes.plot([], [], **kwargs)
        self._x = []
        self._y = []

    def update(self, x, y):
        self._x.append(x)
        self._y.append(y)

        if self.datapoint_limit is not None:
            self._x = self._x[-self.datapoint_limit:]
            self._y = self._y[-self.datapoint_limit:]

        self._line.set_data(self._x, self._y)