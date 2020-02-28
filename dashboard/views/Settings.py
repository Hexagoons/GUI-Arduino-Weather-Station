import tkinter as tk
from tkinter import ttk
import json

from dashboard.entities.Header import Header
from dashboard.entities.Devices import Devices
from dashboard.entities.DeviceInfo import DeviceInfo


class Settings(ttk.Frame):
    """
    Settings view for Application window
    """
    def __init__(self, parent, connected):
        """
        Constructs a Settings View
        :param parent: parent frame
        :param connected: connected devices dict
        """
        ttk.Frame.__init__(self, parent)

        frame1 = Header(self, 'Settings')
        frame1.pack(expand=False, fill=tk.X, side='top', anchor='n')

        self.connected = connected

        # Create content frame
        self.content = ttk.Frame(self)

        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(1, weight=1)

        # Create settings sidebar
        self.sidebar = Devices(self.content, self)
        self.sidebar.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="n")

        # Set initial state
        self.show_no_device()

        self.content.pack(expand=False, fill=tk.X, side='top', anchor='n')

        # Set interval to check at runtime for status updates
        self.after(1000, self.updateStatus)

    def updateStatus(self):
        """
        Update status at runtime if needed
        """
        if callable(getattr(self.deviceInfo, "updateStatus", None)):
            self.deviceInfo.updateStatus()

        self.after(1000, self.updateStatus)

    def OpenView(self):
        """
        Update sidebar and raise this frame to the front
        """
        self.deviceInfo.destroy()
        self.load_devices()
        self.sidebar.grid_forget()
        self.sidebar = Devices(self.content, self)
        self.sidebar.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="n")
        self.deviceInfo.pack_forget()
        self.show_no_device()
        self.tkraise()

    def show_view(self, serial_number, devices_frame):
        """
        Create a device info frame and apply it to the devices_frame frame
        :param serial_number: The Serial number of the device
        :param devices_frame: The frame to apply the device info frame onto
        """
        self.deviceInfo.pack_forget()
        self.deviceInfo = DeviceInfo(self.content, serial_number, self.devices[serial_number], devices_frame, self.connected, self)
        self.deviceInfo.grid(row=0, column=1, padx=(15, 15), pady=(15, 15), sticky="nsew")
        self.content.pack(expand=False, fill=tk.X, side='top', anchor='n')

    def show_no_device(self):
        """
        Show "Geen device geselecteerd" instead of a device info frame
        """
        self.deviceInfo = ttk.Label(self.content, text="Geen device geselecteerd", font=("Verdana", 12))
        self.deviceInfo.grid(row=0, column=1, padx=(15, 15), pady=(15, 15), sticky="nsew")
        self.content.pack(expand=False, fill=tk.X, side='top', anchor='n')

    def load_devices(self):
        """
        Opens the settings file
        """
        jsonFile = open("config/settings.json", "r")
        self.devices = json.load(jsonFile)

    def update_device(self, serial_number, data):
        """
        Updates the settings file
        :param serial_number: Serial number of the device
        :param data:          Data to override
        """
        self.devices[serial_number] = data
        with open('config/settings.json', 'w') as outfile:
            json.dump(self.devices, outfile)

    def delete_device(self, serial_number):
        """
        Delete a device from json by serial number
        :param serial_number: Serial number of the device
        """
        del self.devices[serial_number]
        with open('config/settings.json', 'w') as outfile:
            json.dump(self.devices, outfile)

