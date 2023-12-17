import io
import logging
import struct
from PIL import Image


class DIY:
    def __init__(self, mtu_size):
        self.mtu_size = mtu_size

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

    def splitIntoMultipleLists(self, list_, max_elems_per_list):
        """
        Returns a list containing lists with the elements from `list_`.
        It is ensured that the lists have a maximum length of `max_elems_per_list`.

        Derived from `private List<byte[]> getSendData4096(byte[] bArr)`
        in `com/tech/idotmatrix/core/data/ImageAgreement1.java:259`.
        """
        chunks = []
        len_ = len(list_)
        for start in range(0, len_, max_elems_per_list):
            end = start + min(len_ - start, max_elems_per_list)
            chunks.append(list_[start:end])
        return chunks

    def sendDIYMatrix(self, img: Image.Image):
        """
        Returns a list of byte arrays to be sent individually to the device,
        which once sent will bring the device to display the specified image.

        Derived from `public void sendDIYImageData(BleDevice bleDevice, byte[] bArr, int i, TextAgreementListener textAgreementListener)`
        in `com/tech/idotmatrix/core/data/ImageAgreement1.java:177`.
        """
        payloads = []

        if img.size[0] > 32 or img.size[1] > 32:
            raise Exception('Image needs to be smaller than 32 pixels in width and height.')
        elif img.size[0] != img.size[1]:
            raise Exception('Image needs to be square.')
        # TODO ensure it has the exact format needed by the currently connected device

        # compress image to PNG
        png_buf = io.BytesIO()
        img.save(png_buf, format='PNG')
        png_complete = png_buf.getvalue()

        # make 4096 byte chunks out of the compressed image
        png_chunks = self.splitIntoMultipleLists(png_complete, 4096)

        # arbitrary metadata number
        idk = len(png_complete) + len(png_chunks) * 9  # no idea what the 9 tells us

        # convert some metadata to byte form
        png_len_bytes = struct.pack('i', len(png_complete))
        idk_bytes = struct.pack('h', idk)  # convert to 16bit signed int

        for i in range(len(png_chunks)):
            payload = idk_bytes + bytearray([
                0,
                0,
                2 if i > 0 else 0
            ]) + png_len_bytes + png_chunks[i]
            payloads.append(payload)

        # At this point, the original code got me confused...
        # In `ImageAgreement1.java:158` there is a really weird loop that breaks after the first iteration.
        # That's why it just takes the first payload (so the first 4096 byte PNG chunk + some metadata) and sends it.
        # The rest is discarded - but why did we do this elaborate process in the first place then!?
        # Maybe the decompiler made some mistake, or the original code does not make a ton of sense to begin with.

        # split byte array into multiple MTUs
        return self.splitIntoMultipleLists(payloads[0], self.mtu_size)
