import tkinter as tk
from tkinter import ttk
import json

from dashboard.entities.InputField import InputField
from dashboard.entities.StatusField import StatusField
from dashboard.entities.Devices import Devices
from dashboard.entities.WarningPopUp import WarningPopUp

class DeviceInfo(ttk.Frame):
    """
    DeviceInfo Frame for Settings
    """
    def __init__(self, parent, serial_number, data, devices_frame, connected, settings):
        """
        Constructs a DeviceInformation Frame
        :param parent: Parent Frame
        :param serial_number:   Serial number of the selected device
        :param data:   data of the selected device
        :param devices_frame: Devices Frame 
        :connected: connected status
        :settings: settings class
        """
        ttk.Frame.__init__(self, parent, relief="raised", borderwidth=2)

        self.settings = settings
        self.devices_frame = devices_frame
        self.connected = connected
        self.serial_number = serial_number

        self.content = ttk.Frame(self, borderwidth=2)
        self.content.pack(expand=True, fill=tk.X, side='top')

        label1 = tk.Label(self.content, text=data["Name"], font=("Verdana", 14), relief="groove")
        label1.pack(expand=True, fill=tk.X, side='top')

        if self.serial_number in connected['devices']:
            device = connected['devices'][serial_number]
            self.status = StatusField(self.content, device.status.status)
        else:
            self.status = StatusField(self.content, 'Not connected')

        self.status.pack(expand=True, fill=tk.X, side='top', pady=10)

        self.inputfield = InputField(self.content, "Drempelwaarde Min: ", data["Drempelwaarde"])
        self.inputfield.pack(expand=True, fill=tk.X, side='top', pady=5)

        self.inputfield1 = InputField(self.content, "Drempelwaarde Max: ", data["DrempelwaardeMax"])
        self.inputfield1.pack(expand=True, fill=tk.X, side='top', pady=5)

        self.inputfield2 = InputField(self.content, "Lengthe device in Cm: ", data["Ultrasonesensor"])
        self.inputfield2.pack(expand=True, fill=tk.X, side='top', pady=5)

        button1 = ttk.Button(self, text="Submit", command=lambda: self.submit(serial_number, data))
        button1.pack(expand=True, fill=tk.X, side='top', pady=5)

        button2 = ttk.Button(self, text="Delete device", command=lambda: self.delete_device(serial_number, data))
        button2.pack(expand=True, fill=tk.X, side='top', pady=5)

    def updateStatus(self):
        # Update device status
        if self.serial_number in self.connected['devices']:
            status = self.connected['devices'][self.serial_number].status.status
        else:
            status = 'Not Connected'

        if self.status.status != status:
            self.status.setStatus(status)

    def submit(self, serial_number, data):
        # submit new treshhold and save them in the json and send them to the device
        drempelwaarde = float(self.inputfield.getValue())
        drempelwaardeMax = float(self.inputfield1.getValue())
        if drempelwaarde > drempelwaardeMax:
            WarningPopUp(self, "drempelwaarde")
            return
        ultrasonesensor = self.inputfield2.getValue()

        if serial_number in self.connected['devices']:
            device = self.connected['devices'][serial_number]
            device.protocol.command(0xB0, args=device.protocol.floatToByteArray(float(drempelwaarde)))
            device.protocol.command(0xD0, args=device.protocol.floatToByteArray(float(drempelwaardeMax)))
            device.protocol.command(0xC8, args=device.protocol.floatToByteArray(float(ultrasonesensor)))

        data["Drempelwaarde"] = self.inputfield.getValue()
        data["DrempelwaardeMax"] = self.inputfield1.getValue()
        data["Ultrasonesensor"] = self.inputfield2.getValue()
        self.settings.update_device(serial_number, data)

    def delete_device(self, serial_number, data):
        # delete device
        if self.status.status == 'Not Connected':
            self.settings.delete_device(serial_number)
            self.devices_frame.render_devices()
            self.settings.show_no_device()