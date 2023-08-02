# import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
import numpy as np


class PyGraf(Figure):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _save(self, file_name):
        self.savefig(f'{file_name}.png', format='png')

    def represent_chart(self):
        buf = io.BytesIO()
        self.savefig(buf, format="png")
        return base64.b64encode(buf.getbuffer()).decode("ascii")


class Line(PyGraf):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_tight_layout(True)
        self.ax = self.subplots()
    
    def plot(self, x_axis, y_axis, color, label):
        self.ax.grid(True)
        self.ax.plot(x_axis, y_axis, marker='.' , color=color, label=label) # line chart
        # self.ax.xaxis.set_ticks(x_axis)
        # self.ax.yaxis.set_ticks(y_axis)
        # self.ax.margins(x=0, y=0)
        self.ax.legend()


class Histogram(PyGraf):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_tight_layout(True)
        self.ax = self.subplots()
    
    def plot(self, values, bins, label):
        self.ax.grid(True, linestyle=':', linewidth=1)
        self.ax.hist(values, bins=bins, label=label, edgecolor='black') # hist chart
        self.ax.axvline(29, color='red', label='avg medan')
        # self.ax.margins(x=0, y=0)
        self.ax.legend()


class Radar(PyGraf):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ax = self.subplots(subplot_kw=dict(polar=True))
        # self.angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    

    def plot(self, labels, values, color, text):
        
        N = len(labels)
        values = values
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        # ax = self.subplots(subplot_kw=dict(polar=True))
        self.ax.set_theta_offset(np.pi / 2)
        self.ax.set_theta_direction(-1)
        self.ax.set_thetagrids(np.degrees(angles[:-1]), labels, size=10, fontweight="bold")
        self.ax.tick_params(pad=10, grid_linestyle=':')
        self.ax.set_rticks(range(0, 16, 2), range(0, 16, 2), color="grey", size=8, fontweight="bold")
        self.ax.set_rlim(bottom=0, top=16)
        self.ax.set_rlabel_position(180 / N)
        self.ax.plot(angles, values, color=color, linewidth=1, label=text)
        self.ax.fill(angles, values, color=color, alpha=0.25)
        self.ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))






# testiranje (cod dolje)

# histogram plot
ages = [18, 19, 21, 25, 26, 26, 30, 32, 38, 45, 55]
bins = range(10, 61, 10)


# radar plot
employee = ["Sam", "Rony", "Albert", "Chris", "Jahrum"]
actual = [7, 3, 5, 6, 14]
actual2 = [3, 4, 2, 8, 5]

# line plot
x = np.arange(0, 10)
y1 = np.array([r**2 for r in x])
y2 = np.array([r**3 for r in x])


# chart = Radar()
# chart.plot(employee, actual, 'red', 'test1')
# chart.plot(employee, actual2, 'blue', 'test2')
# chart._save('test2')

# lchar = Line()
# lchar.plot(x, y1, 'blue', 'test')
# lchar.plot(x, y2, 'red', 'test2')
# lchar._save('test_03')

# hchart = Histogram()
# hchart.plot(ages, bins, 'test')
# hchart._save('hist_02')