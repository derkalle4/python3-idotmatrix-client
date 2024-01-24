# python3 imports
from bleak import BleakClient
import logging
import time

# idotmatrix imports
from .idotmatrix.const import UUID_READ_DATA, UUID_WRITE_DATA


class Bluetooth:
    address = None
    client = None
    mtu_size = None

    def __init__(self, address):
        self.address = address

    async def response_handler(self, sender, data):
        """Simple response handler which prints the data received."""

    async def connect(self):
        print("trying to connect BLE")
        try:
            # create client
            self.client = BleakClient(self.address)
            # connect client
            await self.client.connect()
            # Initialise Response Message Handler
            #await self.client.start_notify(UUID_READ_DATA, self.response_handler)
        except Exception as e:
            if self.client.is_connected:
                self.disconnect()
            return False
        return True

    async def disconnect(self):
        if self.client is not None:
            await self.client.stop_notify(UUID_READ_DATA)
            await self.client.disconnect()

    async def send(self, message):
        # check if connected
        if self.client is None or not self.client.is_connected:
            if not await self.connect():
                return False
        await self.client.write_gatt_char(
            UUID_WRITE_DATA,
            message,
        )
        return True
