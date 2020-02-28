import serial
import serial.tools.list_ports
import struct


class SerialHighIntegrityTransmission:
    """
    SerialHighIntegrityTransmission SHIT protocol implementation
    """
    def __init__(self, port):
        """
        Constructs a SHIT Class
        :param port: Port Device is connected to
        """
        self.port = port
        self.baud_rate = 19200

        # Open serial connection
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=0.5)

    def command(self, command, **k_params):
        """
        Sending a command to port
        :param command: The command as array
        :param k_params: keyword arguments
        :return: command response
        """

        # Create an empty read buffer
        read_buffer = b''

        # Append stop byte and arguments
        # If args is set als key word argument add args to byte array
        if 'args' in k_params:
            full_command = bytearray([command, *k_params['args'], 0xff])
        else:
            full_command = bytearray([command, 0xff])

        # Print command (debug purpose only)
        print([str(hex(x)) for x in full_command])

        # While the read buffer is empty
        while read_buffer == b'':
            # Write full command
            self.ser.write(full_command)

            # Read command
            if command in [0x30, 0x28, 0x10, 0x50, 0x48]:
                read_buffer = self.read(6)
            # Write command
            if command in [0xA8, 0xB0, 0xD0, 0xC8]:
                read_buffer = self.read(2)
            # Get data command
            if command == 0x18:
                read_buffer = self.read(6)
            # Status command
            if command == 0x00:
                read_buffer = self.read(3)

        # Print response (debug purpose only)
        print([str(hex(x)) for x in read_buffer])
        print('--------')

        # Return the response
        return read_buffer

    def read(self, chunk_size=200):
        """
        https://stackoverflow.com/questions/19161768/pyserial-inwaiting-returns-incorrect-number-of-bytes
        Read "chunk_size" amount of bytes from serial

        :param chunk_size: amount of byte to be read
        :return: read bytes
        """

        # Create an empty buffer
        read_buffer = b''

        while True:
            # Read in chunks. Each chunk will wait as long as specified by
            # timeout. Increase chunk_size to fail quicker
            byte_chunk = self.ser.read(size=chunk_size)
            read_buffer += byte_chunk
            if not len(byte_chunk) == chunk_size:
                break

        return read_buffer

    @staticmethod
    def getConnectedDevices():
        """
        Get all currently connected devices
        :return: Dict with port, name, description and hwid of the devices.
        """
        raw = serial.tools.list_ports.comports()

        return {x.device: {'port': x.device, 'name': x.name, 'description': x.description, 'hwid': x.hwid}
                for i, x in enumerate(raw) if 'Arduino' in x.description}

    @staticmethod
    def byteArrayToFloat(byte1, byte2, byte3, byte4):
        """
        Cast a byte array to an IEEE 32-bit floating point
        :param byte1: The first byte
        :param byte2: The second byte
        :param byte3: The third byte
        :param byte4: The fourth byte
        :return: IEEE 32-bit floating point
        """
        return struct.unpack('f', bytearray([byte1, byte2, byte3, byte4]))[0]

    @staticmethod
    def floatToByteArray(float1):
        """
        Cast a IEEE 32-bit floating point to a byte array
        :param float1: IEEE 32-bit floating point
        :return: Byte array
        """
        return bytearray(struct.pack('f', float1))
