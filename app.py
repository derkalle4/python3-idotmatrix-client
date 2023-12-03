import asyncio
import random
import time

from PIL import Image
from bleak import BleakScanner, BleakClient
from core.bleChronograph import bleChronograph
from core.bleClock import bleClock
from core.bleCommon import bleCommon
from core.bleCountdown import bleCountdown
from core.bleDIY import bleDIY
from core.bleFullscreenColor import bleFullscreenColor
from core.bleMusicSync import bleMusicSync
from core.bleScoreboard import bleScoreboard

# pip3 install bleak -> https://github.com/hbldh/bleak
# async def main():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)
#
#
# asyncio.run(main())

ADDRESS = '28:66:41:22:D2:7D'
UUID_WRITE_DATA = '0000fa02-0000-1000-8000-00805f9b34fb'
UUID_NOTIFY = '0000fa03-0000-1000-8000-00805f9b34fb'


async def connect(address):
    async with BleakClient(address) as client:
        gatt_characteristic = client.services.get_characteristic(UUID_WRITE_DATA)
        mtu_size = gatt_characteristic.max_write_without_response_size
        print('mtu_size = ' + str(mtu_size))

        # for char in client.services.characteristics:
        #     print(char)

        await client.write_gatt_char(
            UUID_WRITE_DATA,
            bleDIY(mtu_size).enter(1)
        )
        time.sleep(1)

        # img = Image.new('RGB', (32, 32), 255)
        # data = img.load()
        # for x in range(32):
        #     for y in range(32):
        #         data[x, y] = (int(x * 255/32), int(y * 255/32), int(x * 255/32))
        img = Image.open('demo.png')

        mtus = bleDIY(mtu_size).sendDIYMatrix(img)
        for mtu in mtus:
            await client.write_gatt_char(
                UUID_WRITE_DATA,
                mtu
            )
            time.sleep(0.05)


if __name__ == "__main__":
    asyncio.run(connect(ADDRESS))
