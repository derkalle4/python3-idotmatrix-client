import logging
import struct
import zlib


class bleDIY:
    def payload(self, i, data, total_data, i2, i3, i4):
        def get_data_type(i):
            data_type_dict = {
                0: bytearray([0, 0]),
                1: bytearray([1, 0]),
                2: bytearray([2, 0]),
                3: bytearray([3, 0]),
                4: bytearray([0, 1]),
                5: bytearray([5, 1]),
                6: bytearray([0, 0]),
            }
            return data_type_dict.get(i, bytearray([0, 0]))

        def should_crc(i):
            return i in {2, 1, 3, 4}

        def change_light(i, b_arr):
            length = len(b_arr)
            for i2 in range(length):
                b_arr[i2] = (b_arr[i2] * i // 100) & 0xFF

        def crc32_checksum(data):
            return zlib.crc32(bytes(data)) & 0xFFFFFFFF

        data_type = get_data_type(i)
        should_crc_value = should_crc(i)

        if i != 5:
            header_size = 9 if i != 4 else 10
        else:
            header_size = 5

        b_arr3 = bytearray(header_size)

        length = len(data) + header_size + (5 if should_crc_value else 0)

        # Payload Size Encoding
        b_arr3[0:2] = struct.pack('<H', length)

        # Payload Data Encoding
        b_arr3[2:4] = data_type
        b_arr3[4] = i2

        if i != 5:
            # Encode length of payload
            b_arr3[5:9] = struct.pack('<I', len(data))

        # Handling Special Case (i4)
        if i4 != 100:
            change_light(i4, data)

        if not should_crc_value:
            # If CRC is not needed, return the concatenation of the header and data
            return b_arr3 + bytes(data)

        # CRC Calculation
        crc_data = total_data if i == 1 or i == 3 else data
        crc_value = crc32_checksum(crc_data)

        # Log CRC32
        print("#1.0# CRC32 src: ", crc_value)

        b_arr4 = bytearray(struct.pack('<I', crc_value))

        if i == 3:
            b_arr4[4] = 2

        # Ensure that data is a bytearray before concatenation
        if not isinstance(data, bytearray):
            data = bytearray(data)

        # Return the concatenation of header, CRC, and data
        return b_arr3 + b_arr4 + data

    def enter(self, mode=1):
        """ Enter the DIY draw mode of the iDotMatrix device.

        Args:
            mode (int): 0 = disable DIY, 1 = enable DIY, 2 = ?, 3 = ?. Defaults to 1.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray([
                5,
                0,
                4,
                1,
                int(mode) % 256
            ])
        except BaseException as error:
            logging.error(
                'could not enter DIY mode: {}'.format(
                    error))

    def sendDIYMatrix(self):
        color_bytes = [
            (255 >> 16) & 0xFF,
            (255 >> 8) & 0xFF,
            255 & 0xFF,
            10,
            10
        ]
        return bytearray(self.payload(4, color_bytes, color_bytes, 42, len(color_bytes), 99))
