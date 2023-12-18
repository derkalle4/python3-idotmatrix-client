# python3 imports
from bleak import BleakClient
import time

# idotmatrix imports
from .idotmatrix.const import UUID_READ_DATA, UUID_WRITE_DATA


class Bluetooth:
    client = None
    mtu_size = None

    async def response_handler(self, sender, data):
        """Simple response handler which prints the data received."""
        output_numbers = list(data)
        print(output_numbers)

    async def connect(self, address):
        self.client = BleakClient(address)
        try:
            await self.client.connect()
            # get mtu size
            gatt_characteristic = self.client.services.get_characteristic(
                UUID_WRITE_DATA
            )
            self.mtu_size = gatt_characteristic.max_write_without_response_size
            # Initialise Response Message Handler
            await self.client.start_notify(UUID_READ_DATA, self.response_handler)
        except Exception as e:
            print(e)
            self.disconnect()
            return False
        return True

    async def disconnect(self):
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
        for data in self.splitIntoMultipleLists(message):
            await self.client.write_gatt_char(
                UUID_WRITE_DATA,
                data,
            )
            time.sleep(0.01)

    async def get_mtu_size(self):
        return self.mtu_size
