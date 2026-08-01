from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

class ChartWidget(FigureCanvas):
    def __init__(self, width: int, height: int, dpi=100):
        self._width = width 
        self._height = height 
        self._dpi = dpi 
        self._axes = {}
        self._charts = {}
        self.fig = Figure(figsize=(self._width, self._height), dpi=self._dpi)
        
        super().__init__(self.fig)

    def axes(self, name: str): 
        if name not in self._axes: raise ValueError(f"Invalid name! The name {name} isn't a subplot")
        return self._axes[name]
    
    def add_subplot(self, name: str, title: str, x_label: str, y_label: str, *args):
        if name in self._axes: raise ValueError(f"The subplot: {name}, already exists, please choose another name.")
        self._axes[name] = self.fig.add_subplot(*args)
        self._axes[name].set_title(title)
        self._axes[name].set_xlabel(x_label)
        self._axes[name].set_ylabel(y_label)

    def add_chart(self, name: str, chart, datapoint_limit: int=None):
        if name not in self._axes: raise ValueError(f"The subplot name doesn't exist, you dont have a subplot named: {name}") 
        if name in self._charts: raise ValueError(f"The chart: {name}, already exists, please choose another name.")
        self._charts[name] = (chart, datapoint_limit)
        return chart 
        
    def update_data(self, name: str, x: object, y: object):
        if name not in self._charts: raise ValueError(f"The chart named: {name}, doesn't exist!")
        chart, limit = self._charts[name]
        axes = self._axes[name]

        _x = list(chart.get_xdata())
        _y = list(chart.get_ydata())
        _x.append(x)
        _y.append(y)

        if limit is not None:
            _x = _x[-limit:]
            _y = _y[-limit:]
        
        chart.set_data(_x, _y)
        axes.relim()
        axes.autoscale_view()
        self.draw_idle()