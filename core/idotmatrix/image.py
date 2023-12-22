import io
import struct
from PIL import Image as PilImage


class Image:
    def show(self, mode=1):
        """Enter the DIY draw mode of the iDotMatrix device.

        Args:
            mode (int): 0 = disable DIY, 1 = enable DIY, 2 = ?, 3 = ?. Defaults to 1.

        Returns:
            _type_: byte array of the command which needs to be sent to the device
        """
        try:
            return bytearray(
                [
                    5,
                    0,
                    4,
                    1,
                    int(mode) % 256,
                ]
            )
        except BaseException as error:
            raise SystemExit("could not enter image mode :(")

    def load_png(self, file_path):
        """Load a PNG file into a byte buffer.

        Args:
            file_path (str): path to file

        Returns:
            file: returns the file contents
        """
        with open(file_path, "rb") as file:
            return file.read()

    def split_into_chunks(self, data, chunk_size):
        """Split the data into chunks of specified size.

        Args:
            data (bytearray): data to split into chunks
            chunk_size (int): size of the chunks

        Returns:
            list: returns list with chunks of given data input
        """
        return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

    def create_payloads(self, png_data):
        """Creates payloads from a PNG file.

        Args:
            png_data (bytearray): data of the png file

        Returns:
            bytearray: returns bytearray payload
        """
        # Split the PNG data into 4096-byte chunks
        png_chunks = self.split_into_chunks(png_data, 4096)
        # Calculate the arbitrary metadata number
        idk = len(png_data) + len(png_chunks)
        idk_bytes = struct.pack("h", idk)  # convert to 16bit signed int
        png_len_bytes = struct.pack("i", len(png_data))
        # build data
        payloads = bytearray()
        for i, chunk in enumerate(png_chunks):
            payload = (
                idk_bytes
                + bytearray(
                    [
                        0,
                        0,
                        2 if i > 0 else 0,
                    ]
                )
                + png_len_bytes
                + chunk
            )
            payloads.extend(payload)
        return payloads

    def upload_unprocessed(self, file_path):
        """uploads an image without further checks and resizes.

        Args:
            file_path (str): path to the image file

        Returns:
            bytearray: returns bytearray payload
        """
        png_data = self.load_png(file_path)
        return self.create_payloads(png_data)

    def upload_processed(self, file_path, pixel_size=32):
        """uploads a file processed and makes sure everything is correct.

        Args:
            file_path (str): path to the image file
            pixel_size (int, optional): amount of pixels (either 16 or 32 makes sense). Defaults to 32.

        Returns:
            bytearray: returns bytearray payload
        """
        try:
            # Open the image file
            with PilImage.open(file_path) as img:
                # Resize the image
                img_resized = img.resize(
                    (pixel_size, pixel_size), PilImage.Resampling.LANCZOS
                )
                # Create a BytesIO object to hold the PNG data
                png_buffer = io.BytesIO()
                # Save the resized image as PNG to the BytesIO object
                img_resized.save(png_buffer, format="PNG")
                # Seek to the start of the PNG buffer
                png_buffer.seek(0)
                # Return the PNG data
                return self.create_payloads(png_buffer.getvalue())
        except IOError as e:
            raise SystemExit("could not process image: {}".format(e))
