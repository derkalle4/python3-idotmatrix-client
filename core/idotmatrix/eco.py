import logging


class Eco:
    """ This class contains code for the eco mode of the iDotMatrix device.
        With this class you can enable or disable the screen and change the brightness automatically depending on the time.
        Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    def setEcoMode(self, flag, start_hour, start_minute, end_hour, end_minute, light):
        """ Sets the eco mode of the device (e.g. turning on or off the device, set the color, ....)

        Args:
            flag (int): currently unknown, seems to be either 1 or 0
            start_hour (int): hour to start
            start_minute (int): minute to start
            end_hour (int): hour to end
            end_minute (int): minute to end
            light (int): the brightness of the screen

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        # new byte[]{10, 0, 2, ByteCompanionObject.MIN_VALUE, (byte) i, (byte) i2, (byte) i3, (byte) i4, (byte) i5, (byte) i6}
        try:
            return bytearray([
                10,
                0,
                2,
                128,
                int(flag) % 256,
                int(start_hour) % 256,
                int(start_minute) % 256,
                int(end_hour) % 256,
                int(end_minute) % 256,
                int(light) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not set the eco mode: {}'.format(
                    error))
