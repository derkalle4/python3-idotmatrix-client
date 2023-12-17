import logging


class Graffiti:
    """ This class contains the Graffiti controls for the iDotMatrix device.
    """

    def setPixelColor(self, r,g,b,x, y):
        """ Set the scoreboard of the device.

        Args:
            r (int): color red value
            g (int): color green value
            b (int): color blue value
            x (int): pixel x position
            y (int): pixel y position

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:       
            return bytearray([
                ###START COMMAND####
                10,
                0,
                5,
                1,
                0,
                ###END COMMAND####
                r, ###COLOR R
                g, ###COLOR G
                b, ###COLOR B
                x, ###PIXEL X
                y  ###PIXEL Y
            ])
        except BaseException as error:
            logging.error(
                'could not update the Graffiti Board: {}'.format(
                    error))
