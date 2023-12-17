import logging
import struct


class Scoreboard:
    """ This class contains the Scorboard management of the iDotMatrix device.
    """

    def setScoreboard(self, count1, count2):
        """ Set the scoreboard of the device.

        Args:
            count1 (int): first counter, max: 999 (buffer overflow, if more! -> maybe RCE? :D)
            count2 (int): second counter, max: 999 (buffer overflow, if more! -> maybe RCE? :D)

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            bytearray_count1 = struct.pack('!h', int(count1))
            bytearray_count2 = struct.pack('!h', int(count2))
            return bytearray([
                8,
                0,
                10,
                128,
                int(bytearray_count1[1]) % 256,
                int(bytearray_count1[0]) % 256,
                int(bytearray_count2[1]) % 256,
                int(bytearray_count2[0]) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not update the scoreboard: {}'.format(
                    error))
