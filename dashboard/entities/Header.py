import tkinter as tk
from tkinter import ttk


class Header(tk.Frame):
    """
    The Header on top of the application window
    """
    def __init__(self, parent, text):
        """
        Constructs a Device Frame
        :param parent: Parent Frame
        :param text:   warning 
        """
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="De Centrale", font=("Verdana", 25))
        label.pack(fill=tk.BOTH, side='left', anchor='w')

        label = tk.Label(self, text=text, anchor="e", font=("Verdana", 12))
        label.pack(expand=True, fill=tk.BOTH, side='right', anchor='e')
