from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

from .charts import *

class ChartWidget(FigureCanvas):
    def __init__(self, width: int, height: int, dpi=100):
        self._axes = {}
        self._charts = {}
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        super().__init__(self.fig)

    def axes(self, name: str): 
        try:
            return self._axes[name]
        except KeyError:
            raise ValueError(f"No subplot named '{name}' exists.")  
    
    def add_subplot(self, name: str, title: str, x_label: str, y_label: str, *args):
        if name in self._axes: raise ValueError(f"The subplot named '{name}' already exists. Please choose another name.")

        axes = self.fig.add_subplot(*args)
        axes.set_title(title)
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)

        self._axes[name] = axes

        return axes

    def _add_chart(self, name: str, chart):
        if name in self._charts: raise ValueError(f"The chart named '{name}' already exists. Please choose another name.")
        self._charts[name] = chart

    def add_line_plot(self, name: str, datapoint_limit: int | None = None, **kwargs):
        chart = LineChart(self.axes(name), datapoint_limit=datapoint_limit, **kwargs)
        self._add_chart(name, chart)
        return chart

    def update_data(self, name: str, x: object, y: object):
        try:
            chart = self._charts[name]
        except KeyError:
            raise ValueError(f"No chart named '{name}' exists.")
        chart.update(x, y)

        axes = self._axes[name]
        axes.relim()
        axes.autoscale_view()
        self.draw_idle()