import tkinter as tk
from tkinter import ttk


class StatusField(ttk.Frame):
    """
    StatusField displays the device status
    """
    def __init__(self, parent, status):
        """
        Constructs an InputField
        :param parent: Parent Frame
        :param status:   Device status 
        """
        ttk.Frame.__init__(self, parent)

        self.borderframe = ttk.Frame(self, borderwidth=2, relief="sunken")
        self.label2 = ttk.Label(self.borderframe, font=("Verdana", 12), anchor='w')
        self.label3 = tk.Label(self.borderframe, anchor="e", width=2)
        self.status = status
        self.setStatus(status)

    def setStatus(self, status):
        # set device statusField
        self.status = status
        self.label2.pack_forget()
        self.label2 = ttk.Label(self.borderframe, text="Status: {}".format(status), font=("Verdana", 12), anchor='w')
        self.label2.pack(fill=tk.BOTH, side='left', anchor='w', padx=5)

        # status is Disconnected
        self.color = "grey"

        if status is "None":
            self.color = "black"

        if status is "Open":
            self.color = "green"
        
        if status is "Closed":
            self.color = "red"

        if status is "Transitioning":
            self.color = "yellow"

        self.label3.pack_forget()
        self.label3 = tk.Label(self.borderframe, anchor="e", bg=self.color, width=2)
        self.label3.pack(expand=True, side='left', anchor='w')

        self.borderframe.pack(side='left', anchor='w')
