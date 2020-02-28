import tkinter as tk


class PopupWindow(object):
    """
    The PopupWindow is used for nameing new devices.
    """
    def __init__(self, master, text):
        """
        Constructs a PopupWindow
        :param master: Parent Frame
        :param text:   text label 
        """
        self.value = ""
        self.top = tk.Toplevel(master)
        self.l = tk.Label(self.top, text=text)
        self.l.pack()
        self.e = tk.Entry(self.top)
        self.e.pack()
        self.b = tk.Button(self.top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        # destroy inputfield value
        self.value = self.e.get()
        self.top.destroy()

    def getValue(self):
        # get value
        return self.value