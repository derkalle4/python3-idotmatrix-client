# python imports
from datetime import datetime
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

    def add_arguments(self, parser):
        # test
        parser.add_argument(
            "--test",
            action="store_true",
            help="run the test function from the command line class",
        )
        # time sync
        parser.add_argument(
            "--sync-time",
            action="store_true",
            help="sync time to device",
        )
        parser.add_argument(
            "--set-time",
            action="store",
            help="optionally set time to sync to device (use with --sync-time)",
        )
        parser.add_argument(
            "--rotate180degrees",
            action="store",
            help="enable 180 degree device rotation (true = enable, false = disable)",
        )
        parser.add_argument(
            "--togglescreen",
            action="store_true",
            help="toggles the screen on or off",
        )

    async def run(self, args):
        if args.address:
            if not await self.bluetooth.connect(args.address):
                raise SystemExit("could not connect to bluetooth")
            self.mtu_size = await self.bluetooth.get_mtu_size()
        else:
            raise SystemExit("no address for device given")
        # arguments which can be run in parallel
        if args.sync_time:
            await self.sync_time(args.set_time)
        if args.rotate180degrees:
            await self.rotate180degrees(args.rotate180degrees)
        if args.togglescreen:
            await self.togglescreen()
        # arguments which cannot run in parallel
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

    async def sync_time(self, argument):
        """Synchronize local time to device"""
        try:
            date = datetime.strptime(argument, "%d-%m-%Y-%H:%M:%S")
        except ValueError:
            raise SystemExit(
                "wrong format of --set-time: please use dd-mm-YYYY-HH-MM-SS"
            )
        await self.bluetooth.send(
            Common().setTime(
                date.year,
                date.month,
                date.day,
                date.hour,
                date.minute,
                date.second,
            )
        )

    async def rotate180degrees(self, argument):
        """rotate device 180 degrees"""
        if argument.lower() == "true":
            await self.bluetooth.send(Common().rotate180degrees(1))
        else:
            await self.bluetooth.send(Common().rotate180degrees(0))

    async def togglescreen(self):
        """toggles the screen on or off"""
        await self.bluetooth.send(Common().toggleScreenFreeze())
