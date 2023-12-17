import logging


class Countdown:
    """ This class contains the management of the Countdown of the iDotMatrix device.
    """
    def setCountdown(self, mode, minutes, seconds):
        """ Sets the countdown (and activates or disables it)

        Args:
            mode (int): mode of the countdown. 0 = disable, 1 = start, 2 = pause, 3 = restart
            minutes (int): minutes to count down from
            seconds (int): seconds to count down from

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                7,
                0,
                8,
                128,
                int(mode) % 256,
                int(minutes) % 256,
                int(seconds) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not set the countdown: {}'.format(
                    error))
