import tkinter as tk
from tkinter import ttk
import io

import matplotlib
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

matplotlib.use("TkAgg")
style.use("tableau-colorblind10")


class Graph(ttk.Frame):
    """
    Graph Frame from matplotlib
    """
    def __init__(self, parent, threshold_min, threshold_max, graph_type):
        """
        Constructs a Graph Frame
        :param parent: Parent Frame
        :param threshold_min: Min threshold value
        :param threshold_max: Max threshold value
        :param graph_type: Type of graph (sensor type)
        """
        ttk.Frame.__init__(self, parent, borderwidth=2)

        # Create figure
        self.f = Figure(figsize=(2, 2), dpi=100)
        self.a = self.f.add_subplot(111)

        # Set thresholds
        self.threshold_min = threshold_min
        self.threshold_max = threshold_max
        self.type = graph_type

        # Define values for axes
        self.x = range(1, 25)
        self.y = [0] * len(self.x)
        self.a.plot(self.x, self.y, color="blue")
        self.textvar = self.a.text(0, 20, '')

        self.anim = None

        # Update all graph data
        self.setMetadata()

        # Add figure to canvas
        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.get_tk_widget().pack(expand=True, fill=tk.X, side='top')

        # Set animation interval
        animation.FuncAnimation(self.f, self.animate, interval=1000)

    def setMetadata(self):
        """
        Set all metadata for axes and titles and thresholds
        """
        self.a.set_title(self.type)
        self.a.axhline(y=self.threshold_min, color="red")
        self.a.axhline(y=self.threshold_max, color="red")
        self.a.set_xlabel('Time')
        if self.type == 'light':
            self.a.set_ylabel('Light')
        else:
            self.a.set_ylabel('Temperature in Celsius')

    def animate(self, i):
        """
        Redraw line every second
        """
        self.a.clear()
        self.a.plot(self.x, self.y)

        self.textvar.remove()
        sio = io.StringIO()
        print("%.2f" % self.y[-1], file=sio)
        self.textvar = self.a.text(0.2, 0.85, sio.getvalue(), ha='center', va='center', transform=self.a.transAxes)

        self.setMetadata()

    def start(self):
        """
        Start animation interval
        """
        self.anim = animation.FuncAnimation(self.f, self.animate, interval=1000)
