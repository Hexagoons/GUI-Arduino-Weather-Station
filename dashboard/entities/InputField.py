import tkinter as tk
from tkinter import ttk


class InputField(ttk.Frame):
    """
    The inputfield is used for setting device settings for example
    """
    def __init__(self, parent, text, value):
        """
        Constructs am InputField
        :param parent: Parent Frame
        :param text:   text label 
        :param value:   initialize value 
        """
        ttk.Frame.__init__(self, parent)
        l1 = ttk.Label(self, text=text, font=("Verdana", 12))
        l1.pack(side='left')
        self.e1 = ttk.Entry(self, width=6)
        self.e1.insert(tk.END, value)
        self.e1.pack(side='left')

    def getValue(self):
        # get value from imputfield
        return self.e1.get()

    def setValue(self, value):
        # set inputfield value
        self.e1.delete(0, tk.END)
        self.e1.insert(tk.END, value)
