from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

class ChartWidget(FigureCanvas):
    def __init__(self, width: int, height: int, dpi=100, chart_datapoints: int=None):
        self._chart_datapoints = chart_datapoints
        self._width = width 
        self._height = height 
        self._dpi = dpi 
        self._axes = None 
        self.fig = Figure(figsize=(self._width, self._height), dpi=self._dpi)
        
        super().__init__(self.fig)

    def add_subplot(self, *args):
        self._axes = self.fig.add_subplot(*args)

    def update_data(self):
        pass 