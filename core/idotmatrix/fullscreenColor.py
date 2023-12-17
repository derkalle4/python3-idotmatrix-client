import logging


class FullscreenColor:
    """ This class contains the management of the iDotMatrix fullscreen color mode.
        Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    def setColor(self, r=0, g=0, b=0):
        """ Sets the fullscreen color of the screen of the device

        Args:
            r (int, optional): color red. Defaults to 0.
            g (int, optional): color green. Defaults to 0.
            b (int, optional): color blue. Defaults to 0.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                7,
                0,
                2,
                2,
                int(r) % 256,
                int(g) % 256,
                int(b) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not set the color: {}'.format(
                    error))
