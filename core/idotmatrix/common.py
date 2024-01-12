from datetime import datetime
import logging


class Common:
    """This class contains generic bluetooth functions for the iDotMatrix.
    Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    def toggle_screen_freeze(self) -> bytearray:
        """Freezes or unfreezes the screen.

        Returns:
            byte array of the command which needs to be sent to the device
        """
        return bytearray(
            [
                4, 
                0, 
                3, 
                0
            ]
        )

    def turn_screen_off(self) -> bytearray:
        """Turns the screen off.

        Returns:
            byte array of the command which needs to be sent to the device
        """
        return bytearray(
            [
                5, 
                0, 
                7, 
                1,
                0,
            ]
        )

    def turn_screen_on(self) -> bytearray:
        """Turns the screen on.

        Returns:
            byte array of the command which needs to be sent to the device
        """
        return bytearray(
            [
                5, 
                0, 
                7, 
                1,
                1,
            ]
        )

    def flip_screen(self, flip: bool = True) -> bytearray | None:
        """rotates the screen 180 dregrees

        Args:
            flip (bool): False = normal, True = rotated. Defaults to False.
        Returns:
            byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray(
                [
                    5,
                    0,
                    6,
                    128,
                    flip % 256,
                ]
            )
        except BaseException as error:
            logging.error(f"could not rotate the screen of the device: {error}")

    def set_screen_brightness(self, brightness_percent: int) -> bytearray | None:
        """Set screen brightness. Range 5-100 (%)

        Args:
            brightness_percent (int): set the brightness in percent

        Returns:
            byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray(
                [
                    5,
                    0,
                    4,
                    128,
                    brightness_percent % 256,
                ]
            )
        except BaseException as error:
            logging.error(f"could not set the brightness of the screen: {error}")
        
    def set_speed(self, speed: int) -> bytearray | None:
        """Sets the speed of ? - not referenced anywhere in the iDotMatrix Android App.

        Args:
            speed (int): set the speed

        Returns:
            byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray(
                [
                    5,
                    0,
                    3,
                    1,
                    speed % 256,
                ]
            )
        except BaseException as error:
            logging.error(f"could not change the speed of the device: {error}")

    def set_time(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> bytearray | None:
        """Sets the date and time of the device.

        Args:
            year (int): year (4 digits)
            month (int): month
            day (int): day
            hour (int): hour
            minute (int): minute
            second (int): second

        Returns:
            byte array of the command which needs to be sent to the device
        """
        try:
            date = datetime(year, month, day, hour, minute, second)
            return bytearray(
                [
                    11,
                    0,
                    1,
                    128,
                    year % 256,
                    month % 256,
                    day % 256,
                    (date.weekday() + 1) % 256,
                    hour % 256,
                    minute % 256,
                    second % 256,
                ]
            )
        except BaseException as error:
            logging.error(f"could not set the time of the device: {error}")

    def set_joint(self, mode: int) -> bytearray | None:
        """Currently no idea what this is doing.

        Args:
            mode (int): set the joint mode

        Returns:
            byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray(
                [
                    5,
                    0,
                    12,
                    128,
                    mode % 256,
                ]
            )
        except BaseException as error:
            logging.error(f"could not change the device joint: {error}")
            
    def set_password(self, password: int) -> bytearray | None:
        """Setting password: 6 digits in range 000000..999999. Reset device to clear

        Args:
            password (int): password
        Returns:
            byte array of the command which needs to be sent to the device
        """
        
        pwd_high = password // 10000
        pwd_mid = password % 10000 // 100
        pwd_low = password % 100
        
        try:
            return bytearray(
                [
                    8,
                    0,
                    4,
                    2,
                    1,
                    pwd_high,
                    pwd_mid,
                    pwd_low,
                ]
            )
        except BaseException as error:
            logging.error(f"could not set the password: {error}")

