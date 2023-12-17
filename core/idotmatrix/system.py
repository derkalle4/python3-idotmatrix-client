from cryptography.fernet import Fernet


class System:
    """ This class contains system calls for the iDotMatrix device
    """

    def deleteDeviceData(self):
        """ Deletes the device data and resets it to defaults.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        return bytearray([17, 0, 2, 1, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    def encrypt_aes(self, data, key):
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        return encrypted_data

    def getDeviceLocation(self):
        """ Gets the device location (untested yet). Missing some AES encryption stuff of iDotMatrix to work.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        command = bytearray([6, 76, 79, 67, 65, 84, 69, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        return self.encrypt_aes(command, command)
