import logging


class Clock:
    """ This class contains the management of the iDotMatrix clock.
    Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    def setTimeIndicator(self, enabled=True):
        """ Sets the time indicator of the clock. Does not seem to work currently (maybe in a future update?).
            It is inside the source code of BleProtocolN.java, but not referenced anywhere.

        Args:
            enabled (bool, optional): Whether or not to show the time indicator of the clock. Defaults to True.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                5,
                0,
                7,
                128,
                1 if enabled else 0
            ])
        except BaseException as error:
            logging.error(
                'could not set the time indicator: {}'.format(
                    error))

    def setClockMode(self, style, visibleDate, hour24, r=255, g=255, b=255):
        """set the clock mode of the device

        Args:
            style (int): style of the clock
                        0 = default
                        1 = christmas
                        2 = racing
                        3 = inverted full screen
                        4 = animated hourglass
                        5 = frame 1
                        6 = frame 2
                        7 = frame 3
            visibleDate (bool): whether the date should be shown ornot
            hour24 (bool): 12 or 24 hour format
            r (int, optional): color red. Defaults to 255.
            g (int, optional): color green. Defaults to 255.
            b (int, optional): color blue. Defaults to 255.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                8,
                0,
                6,
                1,
                (style | (128 if visibleDate else 0)) | (64 if hour24 else 0),
                int(r) % 256,
                int(g) % 256,
                int(b) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not set the clock mode: {}'.format(
                    error))
