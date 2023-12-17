import logging


class MusicSync:
    def setMicType(self, type):
        """ Set the microphone type. Not referenced anywhere in the iDotMatrix Android App. So not used atm.

        Args:
            type (int): type of the Microphone. Unknown what values can be used.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                6,
                0,
                11,
                128,
                int(type) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not set the microphone type: {}'.format(
                    error))

    def sendImageRythm(self, value1):
        """ Set the image rythm. Not referenced anywhere in the iDotMatrix Android App. When used (tested with values up to 10)
            it displays a stick figure which dances if the value1 gets changed often enough to a different one. 

        Args:
            value1 (int): type of the rythm? Unknown what values can be used.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                6,
                0,
                0,
                2,
                int(value1) % 256,
                1
            ])
        except BaseException as error:
            logging.error(
                'could not set the image rythm: {}'.format(
                    error))

    def sendRhythm(self, mode, byteArray):
        """ Used to send synchronized Microphone sound data to the device and visualizing it. Is handled in MicrophoneActivity.java of the
            iDotMatrix Android App. Will not be implemented here because I have no plans to support the computer microphone. The device
            has an integrated microphone which is able to react to sound.

        Args:
            mode (int): mode of the rythm.
            byteArray (byteArray): actual microphone sound data for the visualization.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return byteArray
        except BaseException as error:
            logging.error(
                'could not set the rythm: {}'.format(
                    error))

    def stopRythm(self):
        """ Stops the Microhpone Rythm on the iDotMatrix device.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        return bytearray([6, 0, 0, 2, 0, 0])
