import tkinter as tk


class WarningPopUp(object):
    def __init__(self, master, warning):

        if warning is "drempelwaarde":
            warning = "De ingevoerde min drempelwaarde mag" + "\n" + "niet hoger zijn dan de max drempelwaarde."
        self.top = tk.Toplevel(master)
        self.l = tk.Label(self.top, text=warning, fg="red")
        self.l.pack()
        # self.e = tk.Entry(self.top)
        # self.e.pack()
        # self.b = tk.Button(self.top, text='Ok', command=self.cleanup)
        #self.b.pack()

    # def cleanup(self):
    #     self.value = self.e.get()
    #     self.top.destroy()

    # def getValue(self):
    #     return self.value