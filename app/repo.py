# import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
import numpy as np

# Generate the figure **without using pyplot**.
fig = Figure()
ax = fig.subplots()
x = [1, 2, 3]
y = np.array([[1, 2], [3, 4], [5, 6]])
ax.plot(x,y)
# Save it to a temporary buffer.
# buf = io.BytesIO()
# fig.savefig(buf, format="png")
# # Embed the result in the html output.
# data = base64.b64encode(buf.getbuffer()).decode("ascii")
# fig.savefig('test.png', format='png')


class PyGraf(Figure):

    def __init__(self, ax1, ax2, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ax1 = ax1
        self.ax2 = ax2
        

    def _subs(self):

        ax = self.subplots()
        # ax.grid(True, linestyle=':', linewidth=1)
        # ax.hist(self.ax1, bins=5, label='test', edgecolor='black') # hist chart
        # ax.pie(self.ax1) # pie chart
        ax.plot(self.ax1, self.ax2, label='test') # line chart
        ax.legend()

    def radar_chart(self):
        num_vars = len(self.ax1)
        values = self.ax2
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        ax = self.subplots(subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi /2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), self.ax1)
        ax.set_ylim(0, 16)
        ax.set_rlabel_position(180 / num_vars)
        ax.plot(angles, values, color='red', linewidth=1)
        ax.fill(angles, values, color='red', alpha=0.25)


    def _save(self):
        self.savefig('bar_01.png', format='png')

    def represent_chart(self):
        buf = io.BytesIO()
        self.savefig(buf, format="png")
        return base64.b64encode(buf.getbuffer()).decode("ascii")



ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752]

employee = ["Sam", "Rony", "Albert", "Chris", "Jahrum"]
actual = [7, 3, 5, 6, 14]

graf = PyGraf(employee, actual)
graf.radar_chart()
graf._save()
