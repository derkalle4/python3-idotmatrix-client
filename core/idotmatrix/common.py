from datetime import datetime
import logging


class Common:
    """ This class contains generic bluetooth functions for the iDotMatrix.
        Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    def toggleScreenFreeze(self):
        """ Freezes or unfreezes the screen.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        return bytearray([4, 0, 3, 0])

    def rotate180degrees(self, type=0):
        """ rotates the screen 180 dregrees

        Args:
            type (int): 0 = normal, 1 = rotated. Defaults to 0.
        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                5,
                0,
                6,
                128,
                int(type) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not rotate the screen of the device: {}'.format(
                    error))

    def setSpeed(self, speed):
        """ Sets the speed of ? - not referenced anyhwere in the iDotrMatrix Android App.

        Args:
            speed (int): set the speed

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                5,
                0,
                3,
                1,
                int(speed) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not change the speed of the device: {}'.format(
                    error))

    def setTime(self, year, month, day, hour, minute, second):
        """ Sets the date and time of the device.

        Args:
            year (int): year (4 digits)
            month (int): month
            day (int): day
            hour (int): hour
            minute (int): minute
            second (int): second

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            date = datetime(year, month, day, hour, minute, second)
            week = int(date.strftime('%U'))
            return bytearray([
                11,
                0,
                1,
                128,
                int(year) % 256,
                int(month) % 256,
                int(day) % 256,
                int(week) % 256,
                int(hour) % 256,
                int(minute) % 256,
                int(second) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not set the time of the device: {}'.format(
                    error))

    def setJoint(self, mode):
        """ Currently no Idea what this is doing.

        Args:
            mode (int): set the joint mode

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                5,
                0,
                12,
                128,
                int(mode) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not change the device joint: {}'.format(
                    error))
