# python3 imports
from bleak import BleakClient
import logging
import time

# idotmatrix imports
from .idotmatrix.const import UUID_READ_DATA, UUID_WRITE_DATA


class Bluetooth:
    address = None
    client = None
    logging = logging.getLogger("idotmatrix." + __name__)
    mtu_size = None

    def __init__(self, address):
        self.logging.debug("initialize bluetooth for {}".format(address))
        self.address = address

    async def response_handler(self, sender, data):
        """Simple response handler which prints the data received."""
        self.logging.debug("device feedback: {}".format(list(data)))

    async def connect(self):
        self.logging.info("connecting to device")
        try:
            # create client
            self.client = BleakClient(self.address)
            # connect client
            await self.client.connect()
            # get mtu size
            gatt_characteristic = self.client.services.get_characteristic(
                UUID_WRITE_DATA
            )
            self.mtu_size = gatt_characteristic.max_write_without_response_size
            # Initialise Response Message Handler
            await self.client.start_notify(UUID_READ_DATA, self.response_handler)
        except Exception as e:
            self.logging.error(e)
            if self.client.is_connected:
                self.disconnect()
            return False
        return True

    async def disconnect(self):
        self.logging.info("disconnecting from device")
        if self.client is not None:
            await self.client.stop_notify(UUID_READ_DATA)
            await self.client.disconnect()

    def splitIntoMultipleLists(self, data):
        """
        Returns a list containing lists with the elements from `data`.
        It is ensured that the lists have a maximum length of `max_elems_per_list`.

        Derived from `private List<byte[]> getSendData4096(byte[] bArr)`
        in `com/tech/idotmatrix/core/data/ImageAgreement1.java:259`.
        """
        chunks = []
        len_ = len(data)
        for start in range(0, len_, self.mtu_size):
            end = start + min(len_ - start, self.mtu_size)
            chunks.append(data[start:end])
        return chunks

    async def send(self, message):
        # check if connected
        if self.client is None or not self.client.is_connected:
            if not await self.connect():
                return False
        self.logging.debug("sending message(s) to device")
        for data in self.splitIntoMultipleLists(message):
            self.logging.debug("trying to send {}".format(data))
            await self.client.write_gatt_char(
                UUID_WRITE_DATA,
                data,
            )
            time.sleep(0.01)
        return True
