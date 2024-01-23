import io
import logging
from PIL import Image as PilImage
import zlib


class Gif:
    logging = logging.getLogger("idotmatrix." + __name__)

    def load_gif(self, file_path):
        """Load a gif file into a byte buffer.

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

    def create_payloads(self, gif_data):
        """Creates payloads from a GIF file.

        Args:
            gif_data (bytearray): data of the gif file

        Returns:
            bytearray: returns bytearray payload
        """
        # TODO: make this function look more nicely :)
        # Calculate CRC of the GIF data
        crc = zlib.crc32(gif_data)
        # header for gif
        header = bytearray(
            [
                255,
                255,
                1,
                0,
                0,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                5,
                0,
                13,
            ]
        )
        # set length
        header[5:9] = int(len(gif_data) + len(header)).to_bytes(4, byteorder="little")
        # add crc
        header[9:13] = crc.to_bytes(4, byteorder="little")
        # Split the GIF data into 4096-byte chunks
        gif_chunks = self.split_into_chunks(gif_data, 4096)
        # build data
        payloads = bytearray()
        for i, chunk in enumerate(gif_chunks):
            header[4] = 2 if i > 0 else 0
            chunk_len = len(chunk) + len(header)
            header[0:2] = chunk_len.to_bytes(2, byteorder="little")
            payloads.extend(header + chunk)
        return payloads

    def upload_unprocessed(self, file_path):
        """uploads an image without further checks and resizes.

        Args:
            file_path (str): path to the image file

        Returns:
            bytearray: returns bytearray payload
        """
        gif_data = self.load_gif(file_path)
        return self.create_payloads(gif_data)

    def upload_processed(self, file, pixel_size=32):
        """uploads a file processed to make sure everything is correct before uploading to the device.

        Args:
            file_path (str): path to the image file
            pixel_size (int, optional): amount of pixels (either 16 or 32 makes sense). Defaults to 32.

        Returns:
            bytearray: returns bytearray payload
        """
        try:
            # Open the gif file
            with PilImage.open(file) as img:
                # resize each frame of the gif
                frames = []
                try:
                    while True:
                        frame = img.copy()
                        if frame.size != (pixel_size, pixel_size):
                            # Resize the current frame
                            frame = frame.resize(
                                (pixel_size, pixel_size), PilImage.Resampling.NEAREST
                            )
                        # Copy the frame and append it to the list
                        frames.append(frame.copy())
                        # Move to the next frame
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass  # End of sequence
                # Create a BytesIO object to hold the GIF data
                gif_buffer = io.BytesIO()
                # Save the resized image as GIF to the BytesIO object
                frames[0].save(
                    gif_buffer,
                    format="GIF",
                    save_all=True,
                    append_images=frames[1:],
                    loop=1,
                    #duration=img.info["duration"],
                    disposal=2,
                )
                # Seek to the start of the GIF buffer
                gif_buffer.seek(0)
                # Return the GIF data
                return self.create_payloads(gif_buffer.getvalue())
        except IOError as e:
            self.logging.error("could not process gif: {}".format(e))
            quit()
