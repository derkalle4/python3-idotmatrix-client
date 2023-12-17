# python imports
import asyncio
from bleak import BleakClient
from PIL import Image
import time

# idotmatrix imports
from .idotmatrix.const import UUID_READ_DATA, UUID_WRITE_DATA
from .idotmatrix.chronograph import Chronograph
from .idotmatrix.clock import Clock
from .idotmatrix.common import Common
from .idotmatrix.countdown import Countdown
from .idotmatrix.diy import DIY
from .idotmatrix.fullscreenColor import FullscreenColor
from .idotmatrix.musicSync import MusicSync
from .idotmatrix.scoreboard import Scoreboard
from .idotmatrix.graffiti import Graffiti


class CMD:
    def __init__(self, args):
        if args.address:
            asyncio.run(self.connect(args.address))
        else:
            raise SystemExit("no address for device given")

    async def connect(self, address):
        async with BleakClient(address) as client:
            gatt_characteristic = client.services.get_characteristic(UUID_WRITE_DATA)
            mtu_size = gatt_characteristic.max_write_without_response_size
            # Initialise Response Message Handler
            await client.start_notify(UUID_READ_DATA, self.notification_handler)

            # for char in client.services.characteristics:
            #    time.sleep(2)
            #    print(char)

            # expect a 50411 response message from this call
            print("mtu_size = " + str(mtu_size))

            # for char in client.services.characteristics:
            #     print(char)

            time.sleep(1)
            # load graffiti board and color pixel 0,0 red
            await client.write_gatt_char(
                UUID_WRITE_DATA, Graffiti().setPixelColor(255, 0, 0, 0, 0)
            )
            # load graffitti board and color pixel 1,1 green
            await client.write_gatt_char(
                UUID_WRITE_DATA, Graffiti().setPixelColor(0, 255, 0, 1, 1)
            )
            # load graffitti board and color pixel 2,2 blue
            await client.write_gatt_char(
                UUID_WRITE_DATA, Graffiti().setPixelColor(0, 0, 255, 2, 2)
            )

            time.sleep(1)
            await client.write_gatt_char(UUID_WRITE_DATA, DIY(mtu_size).enter(1))
            # img = Image.new('RGB', (32, 32), 255)
            # data = img.load()
            # for x in range(32):
            #     for y in range(32):
            #         data[x, y] = (int(x * 255/32), int(y * 255/32), int(x * 255/32))
            img = Image.open("demo.png")

            mtus = DIY(mtu_size).sendDIYMatrix(img)
            for mtu in mtus:
                await client.write_gatt_char(UUID_WRITE_DATA, mtu)
                time.sleep(0.05)

            await client.stop_notify(UUID_READ_DATA)

    # Response Message Handler
    def notification_handler(self, sender, data):
        """Simple notification handler which prints the data received."""
        output_numbers = list(data)
        print(output_numbers)
