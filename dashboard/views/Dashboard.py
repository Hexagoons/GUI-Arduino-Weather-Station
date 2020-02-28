import tkinter as tk
from tkinter import ttk

from dashboard.entities.Header import Header
from dashboard.entities.Device import Device
from dashboard.entities.ScrollableFrame import ScrollableFrame
from libs.SHIT import *


class Dashboard(ttk.Frame):
    """
    Dashboard view for Application window
    """
    def __init__(self, parent, connected):
        """
        Constructs a Dashboard View
        :param parent: parent frame
        :param connected: connected devices dict
        """
        ttk.Frame.__init__(self, parent)

        # Search for connected devices
        self.connected = connected
        self.connected_devices = SerialHighIntegrityTransmission.getConnectedDevices()

        # Initialize grid values
        self.row = 0
        self.column = 0
        self.devices = {}

        # Adding header to frame
        header = Header(self, 'Dashboard')
        header.pack(expand=False, fill=tk.X, side='top', anchor='n')

        # Creating a scrollable content frame
        self.content = ScrollableFrame(self)
        self.content.pack(expand=False, fill=tk.X, side='top', anchor='n')

        # Only create the label don't attach it to the frame
        # attachment is handled by renderDevices method
        self.noDevicesConnected = ttk.Label(self.content.scrollable_frame, text="Geen devices aangesloten",
                                            font=("Verdana", 25))

        # Add all connected devices to the content frame
        for port in self.connected_devices.keys():
            self.addDevice(self.content.scrollable_frame, port)

        # Update the "connected' dict that is passed by reference
        self.updateReference()

        # Render all devices correctly with grid
        self.renderDevices()

        # Set interval for searching newly connected devices
        self.after(1000, self.searchDevices)

        # Poll status and sensor data from device
        self.pollDataFromDevices()

    def OpenView(self):
        """
        Update threshold values in graph and raise this frame to the front
        :return:
        """
        for device in self.devices.values():
            settings = device.load_settings()
            threshold = float(settings[device.serial_number]['Drempelwaarde'])
            thresholdMax = float(settings[device.serial_number]['DrempelwaardeMax'])

            if device.threshold_min != threshold or device.threshold_max != thresholdMax:
                device.updateThresholds(threshold, thresholdMax)

        self.tkraise()

    def searchDevices(self):
        """
        Search for newly connected devices
        """

        # Search for all connected devices
        connected_devices = SerialHighIntegrityTransmission.getConnectedDevices()

        # Use sets to determine differences in new and old data
        removed_devices = self.connected_devices.keys() - connected_devices.keys()
        new_devices = connected_devices.keys() - self.connected_devices.keys()

        # Add new devices
        for key in new_devices:
            self.addDevice(self.content.scrollable_frame, key)

        # Remove and close serial connection removed devices
        for key in removed_devices:
            self.removeDevice(key)

        # Rerender grid
        self.renderDevices()

        # Update reference
        self.connected_devices = connected_devices

        # Update connected dict that is passed by reference
        self.updateReference()

        # Set interval to search new devices
        self.after(1000, self.searchDevices)

    def updateReference(self):
        """
        Update connected dict that is passed by reference
        """
        self.connected['devices'] = {}
        for device in self.devices.values():
            self.connected['devices'][device.serial_number] = device

    def renderDevices(self):
        """
        (Re)render grid for all devices
        """
        self.row = 0
        self.column = 0

        for key in self.devices.keys():
            (self.devices[key]).grid(row=self.row, column=self.column, padx=(15, 15), pady=(15, 15))
            if self.column == 0:
                self.column += 1
            else:
                self.row += 1
                self.column = 0

        # Show no connected devices Label
        if len(self.devices) == 0:
            self.noDevicesConnected.grid(row=0, column=0)
        else:
            self.noDevicesConnected.grid_forget()

        self.content.pack(expand=True, fill=tk.X, side='top')

    def addDevice(self, frame, port):
        """
        Create a Device frame for newly found devices
        :param frame: Parent frame
        :param port:  Port device is connected to
        """
        new_device = Device(frame, port)

        self.devices[port] = new_device

    def removeDevice(self, key):
        """
        Close serial connection and remove device from grid
        :param key: Key in devices array
        """
        if key in self.devices.keys():
            device = self.devices[key]
            device.protocol.ser.close()
            device.grid_forget()
            del self.devices[key]

    def pollDataFromDevices(self):
        """
        Poll status and sensor data from device over serial
        """
        for device in self.devices.values():
            status = "Not Connected"

            try:
                # Read status
                status = device.protocol.command(0x00)
                status = device.protocol.byteArrayToFloat(status[1], status[2], status[3], status[4])

                # Read sensor value
                value = device.protocol.command(0x10)
                value = device.protocol.byteArrayToFloat(value[1], value[2], value[3], value[4])

                # Update graph
                device.graph1.y.pop(0)
                device.graph1.y.append(value)
            except serial.serialutil.SerialException:
                pass

            # Update status Label
            if not status == -1:
                if status == 0:
                    status = "None"
                if status == 1:
                    status = "Closed"
                if status == 2:
                    status = "Open"
                if status == 3:
                    status = "Transitioning"

                if device.status.status != status:
                    device.updateStatus(status)

        # Set interval to poll data again
        self.after(5000, self.pollDataFromDevices)
