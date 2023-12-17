# python imports
from PIL import Image
import time

# idotmatrix imports
from .bluetooth import Bluetooth
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
    bluetooth = Bluetooth()
    mtu_size = None

    async def run(self, args):
        if args.address:
            await self.bluetooth.connect(args.address)
            if not self.bluetooth:
                raise SystemExit("could not connect to bluetooth")
            self.mtu_size = await self.bluetooth.get_mtu_size()
        else:
            raise SystemExit("no address for device given")
        # check for test routine
        if args.test:
            await self.test()

    async def test(self):
        """Tests all available options for the device"""
        ## chronograph
        await self.bluetooth.send(Chronograph().setChronograph(1))
        time.sleep(5)
        await self.bluetooth.send(Chronograph().setChronograph(0))
        time.sleep(1)
        ## clock
        await self.bluetooth.send(Clock().setTimeIndicator(True))
        await self.bluetooth.send(Clock().setClockMode(0, True, True))
        time.sleep(5)
        ## countdown
        await self.bluetooth.send(Countdown().setCountdown(1, 0, 5))
        await self.bluetooth.send(Countdown().setCountdown(0, 0, 5))
        time.sleep(5)
        ## fullscreen color
        await self.bluetooth.send(FullscreenColor().setColor(255, 0, 0))
        time.sleep(5)
        ## scoreboard
        await self.bluetooth.send(Scoreboard().setScoreboard(1, 0))
        time.sleep(1)
        await self.bluetooth.send(Scoreboard().setScoreboard(1, 1))
        time.sleep(1)
        await self.bluetooth.send(Scoreboard().setScoreboard(1, 2))
        time.sleep(1)
        await self.bluetooth.send(Scoreboard().setScoreboard(2, 2))
        ## graffiti
        # load graffiti board and color pixel 0,0 red
        await self.bluetooth.send(Graffiti().setPixelColor(255, 0, 0, 0, 0))
        # load graffitti board and color pixel 1,1 green
        await self.bluetooth.send(Graffiti().setPixelColor(0, 255, 0, 1, 1))
        # load graffitti board and color pixel 2,2 blue
        await self.bluetooth.send(Graffiti().setPixelColor(0, 0, 255, 2, 2))
        time.sleep(5)
        ## diy image (png)
        await self.bluetooth.send(DIY(self.mtu_size).enter(1))
        img = Image.open("demo.png")
        await self.bluetooth.send(DIY(self.mtu_size).sendDIYMatrix(img))
