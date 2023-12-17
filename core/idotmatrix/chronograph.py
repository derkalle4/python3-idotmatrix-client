import logging


class Chronograph:
    def setChronograph(self, mode):
        """Starts/Stops the Chronograph.

        Args:
            mode (int): 0 = reset, 1 = (re)start, 2 = pause, 3 = start after pause

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                5,
                0,
                9,
                128,
                int(mode) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not set the chronograph: {}'.format(
                    error))
