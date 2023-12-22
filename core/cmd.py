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
from .idotmatrix.image import Image
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
            default=datetime.now().strftime("%d-%m-%Y-%H:%M:%S"),
        )
        # device screen rotation
        parser.add_argument(
            "--rotate180degrees",
            action="store",
            help="enable 180 degree device rotation (true = enable, false = disable)",
        )
        # screen toggle
        parser.add_argument(
            "--togglescreen",
            action="store_true",
            help="toggles the screen on or off",
        )
        # chronograph
        parser.add_argument(
            "--chronograph",
            action="store",
            help="sets the chronograph mode: 0 = reset, 1 = (re)start, 2 = pause, 3 = continue after pause",
        )
        # clock
        parser.add_argument(
            "--clock",
            action="store",
            help="sets the clock mode: 0 = default, 1 = christmas, 2 = racing, 3 = inverted full screen, 4 = animated hourglass, 5 = frame 1, 6 = frame 2, 7 = frame 3",
        )
        parser.add_argument(
            "--clock-with-date",
            action="store_true",
            help="shows the current date in addition to the current time.",
        )
        parser.add_argument(
            "--clock-24h",
            action="store_true",
            help="shows the current time in 24h format.",
        )
        parser.add_argument(
            "--clock-color",
            action="store",
            help="sets the color of the clock. Format: <R0-255>-<G0-255>-<B0-255> (example: 255-255-255)",
            default="255-255-255",
        )
        # countdown
        parser.add_argument(
            "--countdown",
            action="store",
            help="sets the countdown mode: 0 = disable, 1 = start, 2 = pause, 3 = restart",
        )
        parser.add_argument(
            "--countdown-time",
            action="store",
            help="sets the countdown mode: <MINUTES>-<SECONDS> (example: 10-30)",
            default="5-0",
        )
        # fullscreen color
        parser.add_argument(
            "--fullscreen-color",
            action="store",
            help="sets a fullscreen color. Format: <R0-255>-<G0-255>-<B0-255> (example: 255-255-255)",
        )
        # pixel color
        parser.add_argument(
            "--pixel-color",
            action="append",
            help="sets a pixel to a specific color. Could be used multiple times. Format: <PIXEL-X>-<PIXEL-Y>-<R0-255>-<G0-255>-<B0-255> (example: 0-0-255-255-255)",
            nargs="+",
        )
        # scoreboard
        parser.add_argument(
            "--scoreboard",
            action="store",
            help="shows the scoreboard with the given scores. Format: <0-999>-<0-999>",
        )
        # image upload
        parser.add_argument(
            "--image",
            action="store",
            help="enables or disables the image mode (true = enable, false = disable)",
        )
        parser.add_argument(
            "--set-image",
            action="store",
            help="uploads a given image file (fastest is png, max. pixel depending on your display). Format: ./path/to/image.png",
        )
        parser.add_argument(
            "--process-image",
            action="store",
            help="processes the image instead of sending it raw (useful when the size does not match or it is not a png). Format: <AMOUNT_PIXEL>",
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
        elif args.chronograph:
            await self.chronograph(args.chronograph)
        elif args.clock:
            await self.clock(args)
        elif args.countdown:
            await self.countdown(args)
        elif args.fullscreen_color:
            await self.fullscreenColor(args.fullscreen_color)
        elif args.pixel_color:
            await self.pixelColor(args.pixel_color)
        elif args.scoreboard:
            await self.scoreboard(args.scoreboard)
        elif args.image:
            await self.image(args)

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
        await self.bluetooth.send(Image().show(1))
        await self.bluetooth.send(Image().upload_unprocessed("./demo.png"))

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

    async def chronograph(self, argument):
        """sets the chronograph mode"""
        if int(argument) in range(0, 4):
            await self.bluetooth.send(Chronograph().setChronograph(int(argument)))
        else:
            raise SystemExit("wrong argument for chronograph mode")

    async def clock(self, args):
        """sets the clock mode"""
        if int(args.clock) in range(0, 8):
            color = args.clock_color.split("-")
            if len(color) < 3:
                raise SystemExit("wrong argument for --clock-color")
            await self.bluetooth.send(
                Clock().setClockMode(
                    style=int(args.clock),
                    visibleDate=args.clock_with_date,
                    hour24=args.clock_24h,
                    r=int(color[0]),
                    g=int(color[1]),
                    b=int(color[2]),
                )
            )
        else:
            raise SystemExit("wrong argument for --clock")

    async def countdown(self, args):
        """sets the countdown mode"""
        if not int(args.countdown) in range(0, 4):
            raise SystemExit("wrong argument for --countdown")
        times = args.countdown_time.split("-")
        if not len(times) == 2:
            raise SystemExit("wrong argument for --countdown-time")
        if int(times[0]) < 0 or int(times[0]) > 99:
            raise SystemExit(
                "wrong argument for --countdown-time - minutes must be between 0 and 99"
            )
        if int(times[1]) < 0 or int(times[1]) > 59:
            raise SystemExit(
                "wrong argument for --countdown-time - seconds must be between 0 and 59"
            )
        if int(times[0]) == 0 and int(times[1]) == 0:
            raise SystemExit(
                "wrong argument for --countdown-time - time cannot be zero"
            )
        await self.bluetooth.send(
            Countdown().setCountdown(
                mode=int(args.countdown),
                minutes=int(times[0]),
                seconds=int(times[1]),
            )
        )

    async def clock(self, args):
        """sets the clock mode"""
        if int(args.clock) in range(0, 8):
            color = args.clock_color.split("-")
            if len(color) < 3:
                raise SystemExit("wrong argument for --clock-color")
            await self.bluetooth.send(
                Clock().setClockMode(
                    style=int(args.clock),
                    visibleDate=args.clock_with_date,
                    hour24=args.clock_24h,
                    r=int(color[0]),
                    g=int(color[1]),
                    b=int(color[2]),
                )
            )
        else:
            raise SystemExit("wrong argument for --clock")

    async def fullscreenColor(self, argument):
        """sets a given fullscreen color"""
        color = argument.split("-")
        if len(color) != 3:
            raise SystemExit("wrong argument for --fullscreen-color")
        await self.bluetooth.send(
            FullscreenColor().setColor(
                int(color[0]),
                int(color[1]),
                color[2],
            )
        )

    async def pixelColor(self, argument):
        """sets the given pixel colors"""
        if len(argument) <= 0:
            raise SystemExit("wrong argument for --pixel-color")
        pixels = []
        # get all pixels to set
        for params in argument:
            for pixel in params:
                pixels.append(pixel)
        # validate all pixels and send them
        for pixel in pixels:
            split = pixel.split("-")
            # check if we got all data
            if len(split) != 5:
                raise SystemExit(
                    "need exactly 5 arguments for a single pixel in --pixel-color"
                )
            # TODO: proper check if we are within the pixel range of the device
            # TODO: maybe we can use a delimiter to make use of the MTU size (sending chunks instead of separate requests)
            # TODO: when filling 32x32 pixels it seems to have trouble to send all pixels. One pixel will be "forgotten" somehow
            await self.bluetooth.send(
                Graffiti().setPixelColor(
                    x=int(split[0]),
                    y=int(split[1]),
                    r=int(split[2]),
                    g=int(split[3]),
                    b=int(split[4]),
                )
            )

    async def scoreboard(self, argument):
        """sets given score on the scoreboard and shows it"""
        scores = argument.split("-")
        if len(scores) != 2:
            raise SystemExit("wrong argument for --scoreboard")
        if int(scores[0]) < 0 or int(scores[1]) < 0:
            raise SystemExit("no negative values allowed for --scoreboard")
        if int(scores[0]) > 999 or int(scores[1]) > 999:
            raise SystemExit("exceeded maximum value of 999 for --scoreboard")
        await self.bluetooth.send(
            Scoreboard().setScoreboard(
                count1=int(scores[0]),
                count2=int(scores[1]),
            )
        )

    async def image(self, args):
        """enables or disables the image mode and uploads a given image file"""
        image = Image()
        if args.image == "false":
            await self.bluetooth.send(
                image.show(
                    mode=0,
                )
            )
        else:
            await self.bluetooth.send(
                image.show(
                    mode=1,
                )
            )
            if args.set_image:
                if args.process_image:
                    await self.bluetooth.send(
                        image.upload_processed(
                            file_path=args.set_image,
                            pixel_size=int(args.process_image),
                        )
                    )
                else:
                    await self.bluetooth.send(
                        image.upload_unprocessed(
                            file_path=args.set_image,
                        )
                    )
