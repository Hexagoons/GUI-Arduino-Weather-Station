import tkinter as tk
from tkinter import ttk
import json

from dashboard.entities.Graph import Graph
from dashboard.entities.InputField import InputField
from dashboard.entities.StatusField import StatusField
from dashboard.entities.PopupWindow import PopupWindow
from dashboard.entities.WarningPopUp import WarningPopUp
from libs.SHIT import *


class Device(ttk.Frame):
    """
    Device Frame for Dashboard
    """
    def __init__(self, parent, port):
        """
        Constructs a Device Frame
        :param parent: Parent Frame
        :param port:   Port Device is connected to
        """
        ttk.Frame.__init__(self, parent, relief="raised", borderwidth=2)

        # Initializing serial connection
        self.protocol = SerialHighIntegrityTransmission(port)
        self.port = port

        # Retrieving json settings
        self.settings = self.load_settings()
        data = self.getData()
        self.serial_number = data['serial_number']
        self.type = data['type']

        # Retrieve name or ask for a name
        self.name = self.getName()

        # Sync json data with EEPROM
        self.threshold_min = 0
        self.threshold_max = 0
        self.syncData()

        # Saving device specific settings
        self.deviceSettings = self.settings[data['serial_number']]

        # Creating initial graph
        self.graph1 = Graph(self, self.threshold_min, self.threshold_max, self.type)
        self.graph1.pack(expand=True, fill=tk.X, side='top')
        self.graph1.start()

        # Creating content frame (section under graph)
        self.content = ttk.Frame(self, borderwidth=2)
        self.content.pack(expand=True, fill=tk.X, side='top')

        # Creating components and inputfields for the content frame
        label1 = tk.Label(self.content, text=self.name, font=("Verdana", 14))
        label1.pack(expand=True, fill=tk.X, side='top')

        self.status = StatusField(self.content, "Open")
        self.status.pack(expand=True, fill=tk.X, side='top', pady=10)

        self.inputfield = InputField(self.content, "Drempelwaarde Min: ", self.deviceSettings['Drempelwaarde'])
        self.inputfield.pack(expand=True, fill=tk.X, side='top', pady=5)

        self.inputfield2 = InputField(self.content, "Drempelwaarde Max: ", self.deviceSettings['DrempelwaardeMax'])
        self.inputfield2.pack(expand=True, fill=tk.X, side='top', pady=5)

        submitButton = ttk.Button(self, text="Submit", command=self.updateDevice)
        submitButton.pack(expand=True, fill=tk.X, side='top', pady=5)

    def askForNewDeviceName(self):
        """
        Asks the user for a name for this device
        :return: Filled in value
        """
        w = PopupWindow(self, "Nieuw apparaat gedetecteerd op PORT: {}".format(self.port))
        self.wait_window(w.top)

        return w.getValue()

    def syncData(self):
        """
        Sync json data with EEPROM
        """

        # Retrieve values from json
        drempelwaarde_min = float(self.settings[self.serial_number]['Drempelwaarde'])
        drempelwaarde_max = float(self.settings[self.serial_number]['DrempelwaardeMax'])
        ultrasonesensor = float(self.settings[self.serial_number]['Ultrasonesensor'])

        # Read values from Arduino (EEPROM)
        resp = self.protocol.command(0x30)
        device_drempelwaarde_min = self.protocol.byteArrayToFloat(resp[1], resp[2], resp[3], resp[4])

        resp = self.protocol.command(0x50)
        device_drempelwaarde_max = self.protocol.byteArrayToFloat(resp[1], resp[2], resp[3], resp[4])

        resp = self.protocol.command(0x28)
        device_ultrasonesensor_min = self.protocol.byteArrayToFloat(resp[1], resp[2], resp[3], resp[4])

        resp = self.protocol.command(0x48)
        device_ultrasonesensor_max = self.protocol.byteArrayToFloat(resp[1], resp[2], resp[3], resp[4])

        # Update values of they are not equal to each other
        if drempelwaarde_min != device_drempelwaarde_min:
            self.protocol.command(0xB0, args=self.protocol.floatToByteArray(drempelwaarde_min))

        if drempelwaarde_max != device_drempelwaarde_max:
            self.protocol.command(0xD0, args=self.protocol.floatToByteArray(drempelwaarde_max))

        if device_ultrasonesensor_min != 10.0:
            self.protocol.command(0xA8, args=self.protocol.floatToByteArray(10.0))

        if ultrasonesensor != device_ultrasonesensor_max:
            self.protocol.command(0xC8, args=self.protocol.floatToByteArray(ultrasonesensor))

        # Updated own references
        self.threshold_min = drempelwaarde_min
        self.threshold_max = drempelwaarde_max

    def updateDevice(self):
        """
        Handles "submit" button handler
        """

        # Get values from input fields
        drempelwaarde = float(self.inputfield.getValue())
        drempelwaardeMax = float(self.inputfield2.getValue())

        # Validation
        if drempelwaarde > drempelwaardeMax:
            WarningPopUp(self, "drempelwaarde")
            return

        # Update EEPROM
        self.protocol.command(0xB0, args=self.protocol.floatToByteArray(float(drempelwaarde)))
        self.protocol.command(0xD0, args=self.protocol.floatToByteArray(float(drempelwaardeMax)))

        # Update GUI
        self.updateThresholds(float(drempelwaarde), float(drempelwaardeMax))

        # Update references and json
        self.deviceSettings["Drempelwaarde"] = self.inputfield.getValue()
        self.deviceSettings["DrempelwaardeMax"] = self.inputfield2.getValue()
        self.settings[self.serial_number] = self.deviceSettings
        with open('config/settings.json', 'w') as outfile:
            json.dump(self.settings, outfile)
        pass

    def updateThresholds(self, t_min, t_max):
        """
        Updates threshold in GUI
        :param t_min: Minimum threshold value
        :param t_max: Maximum threshold value
        """

        # Update input fields
        self.inputfield.setValue(t_min)
        self.inputfield2.setValue(t_max)

        # Update references
        self.threshold_min = t_min
        self.threshold_max = t_max

        # Update Graph
        self.graph1.threshold_min = t_min
        self.graph1.threshold_max = t_max

    def getData(self):
        """
        Read serial number and type
        :return: dict with serial_number and type
        """

        # Get Serial number/ Type
        data = self.protocol.command(0x18)

        # Fallback values
        serial_number = []
        sensor = "Licht"

        # Loop trough byte array
        for index in range(len(data)):
            byte = data[index]

            # Skip command and stop byte
            if index in [1, 2, 3, 4]:
                # Generate serial number
                serial_number.append(str(byte))

                # Determine type
                if index is 4 and byte == 1:
                    sensor = "Temperatuur"

        return {
            'serial_number': "-".join(serial_number),
            'type': sensor
        }

    def getName(self):
        """
        Get name from json or ask the user to fill in a name

        :return: Name from json or user provided name
        """

        # Check settings json
        if self.serial_number in self.settings.keys():
            return self.settings[self.serial_number]['Name']

        # Ask new device name popup
        name = self.askForNewDeviceName()

        # Defaults for Temp sensor
        if self.type == 'Temperatuur':
            self.settings[self.serial_number] = {"Name": name, "Drempelwaarde": "15", "DrempelwaardeMax": "20",
                                                 'Ultrasonesensor': '30'}
        # Defaults light sensor
        else:
            self.settings[self.serial_number] = {"Name": name, "Drempelwaarde": "400", "DrempelwaardeMax": "600",
                                                 'Ultrasonesensor': '30'}

        # Add serial number with data to json
        self.update_settings(self.settings)

        return name

    def updateStatus(self, status):
        """
        Updates the status field
        :param status: The new status string
        """
        self.status.setStatus(status)

    @staticmethod
    def load_settings():
        """
        Opens the settings file
        :return: dict with contents from settings file
        """
        with open('config/settings.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def update_settings(settings):
        """
        Updates the settings file
        :param settings: dict that should be saved
        """
        with open('config/settings.json', 'w') as file:
            json.dump(settings, file)
