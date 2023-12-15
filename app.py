import asyncio
import time
from bleak import BleakScanner, BleakClient
from core.bleChronograph import bleChronograph
from core.bleClock import bleClock
from core.bleCommon import bleCommon
from core.bleCountdown import bleCountdown
from core.bleDIY import bleDIY
from core.bleFullscreenColor import bleFullscreenColor
from core.bleMusicSync import bleMusicSync
from core.bleScoreboard import bleScoreboard
from core.bleGraffiti import bleGraffiti

# pip3 install bleak -> https://github.com/hbldh/bleak
# async def main():
#    #devices = await BleakScanner.discover()
#    for d in devices:
#        print(d)

# asyncio.run(main())

address = 'E2:39:3C:0A:6C:68'
UUID_WRITE_DATA = '0000fa02-0000-1000-8000-00805f9b34fb'


async def connect(address):
    async with BleakClient(address) as client:
        gatt_characteristic = client.services.get_characteristic(UUID_WRITE_DATA)
        mtu_size = gatt_characteristic.max_write_without_response_size
        # for char in client.services.characteristics:
        #    time.sleep(2)
        #    print(char)
        await client.write_gatt_char(
            UUID_WRITE_DATA,
            bleDIY().enter(1)
        )

        time.sleep(1)
        #load graffiti board and color pixel 0,0 red
        await client.write_gatt_char(
            UUID_WRITE_DATA,
            bleGraffiti().setPixelColor(255,0,0,0,0)
        )
        #load graffitti board and color pixel 1,1 green
        await client.write_gatt_char(
            UUID_WRITE_DATA,
            bleGraffiti().setPixelColor(0,255,0,1,1)
        )
        #load graffitti board and color pixel 2,2 blue
        await client.write_gatt_char(
            UUID_WRITE_DATA,
            bleGraffiti().setPixelColor(0,0,255,2,2)
        )


        time.sleep(1)
        await client.write_gatt_char(
            UUID_WRITE_DATA,
            bleDIY().sendDIYMatrix()
        )

if __name__ == "__main__":
    asyncio.run(connect(address))
