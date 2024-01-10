# python imports
import os
import logging


class Utils:
    logging = logging.getLogger("idotmatrix." + __name__)

    def write_address(file_path, content):
        """Write address to a file"""
        with open(file_path, "w") as file:
            file.write(content)
            logging.info("Writing the address to a file")

    def check_address(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                line = file.readline()
            os.environ['IDOTMATRIX_ADDRESS'] = line.strip()
            logging.info("Default Address set.")
        else:
            # If the file doesn't exist, you can handle it here or ignore the function call
            logging.debug("There's no address file set.")
            pass
